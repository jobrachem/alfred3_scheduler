# alfred3_scheduler
 
A plugin for alfred3 for managing experiment appointments.

## Installation

Install via pip:

```
$ pip install alfred3_scheduler
```

## Documentation

There is limited API documentation [here](https://jobrachem.github.io/alfred3_scheduler/build/html/index.html).
For a usage example and some notes, see below.

## Usage

The scheduler can be added to an experiment like this:

```python
import alfred3 as al
import alfred3_scheduler as als

exp = al.Experiment()

scheduler = als.Scheduler("demo_scheduler", lang="de")


@exp.member(admin=True)
class SchedulerAdmin(als.SchedulerAdmin):
    scheduler = scheduler


@exp.member
class SchedulerInterface(als.SchedulerInterface):
    scheduler = scheduler
    email = "test@email.address" # for testing purposes, you can put
```


Now, the experiment has three views:

1. The normal view, where the usual experiment can be worked on by participants.
2. The admin view, where administrators can see and manage experiment sessions. Started by
   appending `?admin=true` to the experiment url.
3. The scheduler view, where potential participants can sign up for experiment
   sessions. Started by appending `?scheduler=scheduler_name` to the experiment
   url. In the case of the demo code above, `scheduler_name` would be
   replaced by `demo_scheduler`.


### The SchedulerInterface expects that you know a participant's email

From the documentation of `SchedulerInterface`:

```
email (str): Participant email address. The SchedulerInterface
    expects that you have asked the participant for their
    email address on a previous page. You can provide it on init,
    as a class attribute, or access in :meth:`.on_exp_access`.
    Often, the latter option will be the easiest to use.
```

It is most sensible to initialize a SchedulerInterface only once you 
have already obtained the participant's email address.


### The scheduler needs email configuration

This means, you need to put the following data into secrets.conf:

```
[mail]
address = sender@mail.address
name = Sender Name
password = password
server = smtp.server.com
port = 465 
```

### The scheduler requires alfred3's admin interface to be activated

The admin interface is activated by setting the three levels of
admin passwords in secrets.conf:

```
[general]
adminpass_lvl1 = level1
adminpass_lvl2 = level2
adminpass_lvl3 = level3
```

