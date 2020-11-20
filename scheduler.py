import schedule
import time
import threading
import mattermost
import settings

def validateRequest(req):
    print("HERE TO VALIDATE A REQUEST")
    if(len(req) < 3):
        return False
    isNumValid = req[1].isdigit()
    switcher = {
        'hours':True,
        'minutes':True,
        'days':True,
        'seconds':True
    }
    isTimeValid = False
    isTimeValid = switcher.get(req[2].lower(), False)
    if (isNumValid and isTimeValid is True):
        return True
    return False

class ContinuousScheduler(schedule.Scheduler):
      import settings
      def run_continuously(self, interval=1):
            """Continuously run, while executing pending jobs at each elapsed
            time interval.
            @return cease_continuous_run: threading.Event which can be set to
            cease continuous run.
            Please note that it is *intended behavior that run_continuously()
            does not run missed jobs*. For example, if you've registered a job
            that should run every minute and you set a continuous run interval
            of one hour then your job won't be run 60 times at each interval but
            only once.
            """
            cease_continuous_run = threading.Event()

            class ScheduleThread(threading.Thread):
                @classmethod
                def run(cls):
                    # I've extended this a bit by adding self.jobs is None
                    # now it will stop running if there are no jobs stored on this schedule
                    while not cease_continuous_run.is_set() and self.jobs:
                        # for debugging
                        # print("ccr_flag: {0}, no. of jobs: {1}".format(cease_continuous_run.is_set(), len(self.jobs)))
                        self.run_pending()
                        time.sleep(interval)

            continuous_thread = ScheduleThread()
            continuous_thread.start()
            return cease_continuous_run

# I've added another way you can stop the schedule to the class above
# if all the jobs are gone it stops, and you can remove all jobs with clear()
#your_schedule.clear()

# the third way to empty the schedule is by using Single Run Jobs only
# single run jobs return schedule.CancelJob

def remind(userData):
    import settings
    mmbot = mattermost.MattermostAPI(settings.API_URL, False, settings.BOT_TOKEN)
    channel = userData["channel_id"]
    x = mmbot.create_post(channel, userData)
    print(x)
    return schedule.CancelJob

def scheduleJob(req,userData):
    import settings
    print(req)
    another_schedule = ContinuousScheduler()
    print("trying to schedule this") 
    print(req[2])
    if (req[2] == "seconds"):
        another_schedule.every(int(req[1])).seconds.do(remind, userData)
    elif (req[2] == "minutes"):
        another_schedule.every(int(req[1])).minutes.do(remind, userData)
    elif (req[2] == "hours"):
        another_schedule.every(int(req[1])).hours.do(remind, userData)
    elif (req[2] == "days"):
        another_schedule.every(int(req[1])).days.do(remind, userData)
    else:
        print("couldnt understand")

    print("finished schedule")
    halt_schedule_flag = another_schedule.run_continuously()

