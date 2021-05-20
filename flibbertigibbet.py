import json
from httplib2 import Http
from boto3.session import Session
import time
import random

http_obj = Http()
aws_region = 'us-west-2'
cloudwatch_logs = f'https://{aws_region}.console.aws.amazon.com/cloudwatch/home?region=' \
                  f'{aws_region}#logEventViewer:group=/aws/batch/job'

# Note: this can be a slack endpoint as well. Just fill in your key and token here.
notification_endpoint = 'https://chat.googleapis.com/v1/spaces/AAAAP1u58L8/messages?key=' \
                        'EXAMPLE_KEY&token=EXAMPLE_TOKEN'

wit = [
    "Probably not your fault.",
    "This had nothing to do with you.",
    "It's all part of the learning process.",
    "Oh no.",
    "I have not failed. I've just found 10,000 ways that won't work. ― Thomas A. Edison",
    "Success is not final, failure is not fatal: it is the courage to continue that counts. ― Winston S. Churchill",
    "There is only one thing that makes a dream impossible to achieve: the fear of failure. ― Paulo Coelho, The Alchemist",
    "Pain is temporary. Quitting lasts forever. ― Lance Armstrong",
    "Failure is the condiment that gives success its flavor. ― Truman Capote",
    "Have no fear of perfection - you'll never reach it. ― Salvador Dali",
    "Success is stumbling from failure to failure with no loss of enthusiasm. ― Winston S. Churchill",
    "Do not fear failure but rather fear not trying. ― Roy T. Bennett, The Light in the Heart",
    "It is hard to fail, but it is worse never to have tried to succeed. ― Theodore Roosevelt",
    "All of old. Nothing else ever. Ever tried. Ever failed. No matter. Try again. Fail again. Fail better. ― Samuel Beckett, Worstward Ho",
    "Only those who dare to fail greatly can ever achieve greatly. ― Robert F. Kennedy",
    "Never confuse a single defeat with a final defeat. ― F. Scott Fitzgerald",
    "Together, they would watch everything that was so carefully planned collapse, and they would smile at the beauty of destruction. ― Markus Zusak, The Book Thief"
]

session = Session(region_name='us-west-2')
batch_client = session.client('batch')


def lambda_handler(event, context):

    # parse message
    details = event["detail"]
    if details["status"] not in ["FAILED", "SUCCEEDED"]:
        # ignore cloudwatch events from jobs transitioning from READY -> RUNNING etc
        return 0

    try:
        # grab the Cloudwatch Url for this job - this gets you the callback for debugging
        log_url = cloudwatch_logs + ';stream=' + details['container']['logStreamName']
        cpus = details['container']['vcpus']
        mem = details['container']['memory'] / 1000
        duration = time.strftime("%H:%M", time.gmtime((details['stoppedAt'] - details["startedAt"]) / 1000))
    except KeyError:  # Typical of user-terminated jobs, don't need to keep track of those
        return 0

    # startbuilding message
    message = f"Job {details['jobName']} *{details['status']}* in {duration} hours. " \
              f"*<{log_url}|Cloudwatch Logs>*"

    # add error to message if Failed:
    if details['status'] == 'FAILED':
        try:
            reason = details['attempts'][0]['container']['reason']
        except KeyError:  # Batch container don't always return a 'reason' along the exit code
            reason = details['statusReason']
        message += f"\n*{reason}*"

        if "OutOfMemoryError" in reason:
            # add some handy details on CPU/Ram if container ran out of memory
            message += f' ({cpus}CPU + {mem}GB RAM)'

        # some emotional support for failed jobs.
        message += f'\n_{random.choice(wit)}_'

    send_to_gchat(message)
    return 0


def send_to_gchat(message):
    print("Sending message to gsuck...")
    response = http_obj.request(
            uri=notification_endpoint,
            method='POST',
            headers={'Content-Type': 'application/json; charset=UTF-8'},
            body=json.dumps({'text': message}), )
    print(response)
    return
