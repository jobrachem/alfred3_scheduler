"""Tests for the scheduler module."""
# pylint: disable=redefined-outer-name
# pylint: disable=no-self-use

import datetime

import pytest
from alfred3_interact.scheduler.scheduler import AlreadyRegistered
from alfred3_interact.scheduler.scheduler import DateSlot
from alfred3_interact.scheduler.scheduler import DateSlotData
from alfred3_interact.scheduler.scheduler import ParticipantData
from alfred3_interact.scheduler.scheduler import Participant
from alfred3_interact.scheduler.element import AddDateSlot


@pytest.fixture
def slot(exp):
    """Date slot fixture."""
    date = datetime.datetime(2022, 3, 14, 14, 30)

    data = DateSlotData(date, duration=30, n_participants=3, n_overbook=1, scheduler_id="test")
    yield DateSlot.new(data, exp=exp)


@pytest.fixture
def participant(exp):
    """Participant fixture."""
    data = ParticipantData("test@test.de", scheduler_id="test")
    yield Participant.new(data, exp=exp)


class TestDateSlot:
    """Test date slot functionality."""

    def test_time(self, slot):
        """Tests whether time is handled and printed correctly."""

        assert isinstance(slot.time.startdate(), str)
        assert isinstance(slot.time.enddate(), str)

        start = datetime.datetime.fromtimestamp(slot.time.start)
        end = datetime.datetime.fromtimestamp(slot.time.end)
        assert end - start == datetime.timedelta(minutes=30)

    def test_npending(self, slot, participant):
        """Test if npending gives correct number of participants."""
        assert slot.npending() == 0

        participant.register(slot)
        assert slot.npending() == 1

        participant.cancel_registration(slot)
        assert slot.npending() == 0

    def test_nconfirmed(self, slot, participant):
        """Test whether nconfirmed gives correct number of participants."""
        assert slot.nconfirmed() == 0

        participant.register(slot)
        assert slot.nconfirmed() == 0

        participant.cancel_registration(slot)
        assert slot.nconfirmed() == 0

    def test_nopen(self, slot, participant):
        """Test whether nopen gives correct number of participants."""
        assert slot.nopen() == 4

        participant.register(slot)
        assert slot.nopen() == 3

        participant.confirm_email(slot)
        assert slot.nopen() == 3


class TestParticipant:
    """Tests participant functionality."""

    def test_register(self, slot, participant):
        """Tests whether participant registration works."""
        participant.register(slot)

        slotdata = slot.data_handler.load()
        assert participant.participant_id in slotdata["participants"]

        pdata = participant.data_handler.load()
        assert slot.dateslot_id in pdata["slots"]

    def test_register_twice(self, slot, participant):
        """
        Tests whether exception is correctly raised when trying to register
        for the same slot twice.
        """
        participant.register(slot)
        with pytest.raises(AlreadyRegistered):
            participant.register(slot)

    def test_cancel_registration(self, slot, participant):
        """Tests whether cancelling a registration works."""
        participant.register(slot)
        participant.cancel_registration(slot)

        slotdata = slot.data_handler.load()
        assert participant.participant_id not in slotdata["participants"]

        pdata = participant.data_handler.load()
        assert slot.dateslot_id not in pdata["slots"]

    def test_confirm_email(self, slot, participant):
        """Test whether email confirmation has the intended effect."""
        participant.register(slot)
        participant.confirm_email(slot)

        data = slot.data_handler.load()
        assert data["participants"][participant.participant_id]["confirmed"]

        data = participant.data_handler.load()
        assert slot.dateslot_id in data["confirmed_slots"]


class TestAddDateSlot:

    def test_prepare_slots(self, exp):
        el = AddDateSlot(scheduler="test-sched", name="test")
        el.added_to_experiment(exp)

        default = el.default

        test = ["2022-02-23", "10:43", "100", "5", "3", ""]
        test = ",".join(test)

        data = "\n".join([default, test])

        el.set_data({"test": data})

        slots = el.prepare_slots()

        assert len(slots) == 1
    
    def test_colnames(self, exp):
        el = AddDateSlot(scheduler="test-sched", name="test")
        el.added_to_experiment(exp)

        default = el.default.split(",")
        default[0] = "test"
        default = ",".join(default)


        test = ["2022-02-23", "10:43", "100", "5", "3", ""]
        test = ",".join(test)

        data = "\n".join([default, test])

        el.set_data({"test": data})

        with pytest.raises(ValueError):
            el.prepare_slots()
    

    def test_write_slots(self, exp):
        el = AddDateSlot(scheduler="test-sched", name="test")
        el.added_to_experiment(exp)

        default = el.default

        test = ["2022-02-23", "10:43", "100", "5", "3", ""]
        test = ",".join(test)

        data = "\n".join([default, test])

        el.set_data({"test": data})

        slots = el.prepare_slots()
        result = el.write_slots()

        assert f"{len(slots)}" in result
        assert "Inserted" in result

    def test_write_slots_error(self, exp):
        el = AddDateSlot(scheduler="test-sched", name="test")
        el.added_to_experiment(exp)

        default = el.default
        
        default = el.default.split(",")
        default[0] = "test"
        default = ",".join(default)

        test = ["2022-02-23", "10:43", "100", "5", "3", ""]
        test = ",".join(test)

        data = "\n".join([default, test])

        el.set_data({"test": data})

        result = el.write_slots()

        assert "There was an exception" in result
