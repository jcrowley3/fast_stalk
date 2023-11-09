import greenstalk
import json
import time
from logging_format import init_logger

logger = init_logger()


# Producer's beanstalkd connection to the 'survey_tube'
producer_beanstalk = greenstalk.Client(('127.0.0.1', 11300))
producer_beanstalk.use('survey_tube')
logger.gsd_producer("GSD Producer connected to 'survey_tube'")


def reward_job():
    return {
        "eventType": "REWARD_SCHEDULED",
        "source": "GSD",
        "version": 0,
        "body": {
            "surveyId": "aebQTOSw",
            "experience": {
                "concierge": "Jennifer",
                "name": "Skydiving"
            },
            "recipient": {
                "name": "Jane Doe",
                "email": "jane@doe.com"
            }
        }
    }


def survey_job():
    return {
        "eventType": "GET_SURVEY_RESPONSE",
        "body": {
            "surveyId": "aebQTOSw"
        }
    }

def produce_jobs():
    logger.gsd_producer("Adding jobs...")
    jobs = [
        reward_job(),
        survey_job()
    ]
    for i in range(20):
        for job in jobs:
            producer_beanstalk.put(json.dumps(job))
            # logger.gsd_producer(f"{job['eventType']} job added to 'survey_tube' (Batch: {i+1}/5)")
    logger.gsd_producer("10x jobs added to 'survey_tube'")


def put_job(job):
    producer_beanstalk.put(json.dumps(job))
    logger.gsd_producer(f"{job['eventType']} job added to 'survey_tube'")


def add_job_interactively():
    while True:
        job_type = input(
            "Select the type of job to add to the queue:\n"
            "  1: REWARD_SCHEDULED\n"
            "  2: GET_SURVEY_RESPONSE\n"
            "  3: Exit\n"
            "----------------\n"
            "Your choice: "
        )

        match job_type:
            case '1':
                job = reward_job()
                put_job(job)
            case '2':
                job = survey_job()
                put_job(job)
            case '3':
                break
            case _:
                print("Invalid selection.")


if __name__ == '__main__':
    last_job_count = None

    while True:
        job_total = producer_beanstalk.stats_tube('survey_tube')['current-jobs-ready']

        if job_total != last_job_count:
            if job_total <= 20:
                logger.gsd_producer(f"only {job_total} jobs left!!!")
                produce_jobs()
            else:
                logger.gsd_producer(f"{job_total} jobs in tube")

            last_job_count = job_total

        time.sleep(5)


    # add_job_interactively()
