import pytest
from mockito import ANY, when, mock, unstub
import sys
import os
sys.path.insert(0, os.getcwd())
from robobrowser import RoboBrowser
from source import missedClassScrapper

def test_invalid_credentials():

	browser = missedClassScrapper.network("16CSVWXYZ","password")
	assert browser is None

def test_missed_class_dates():

	result = missedClassScrapper.MissedClassDates("16CSVWXYZ","password","2019-07-19")
	assert not result
	browser = RoboBrowser(history=False, parser='html.parser')
	when(missedClassScrapper).network(...).thenReturn(browser)
	with pytest.raises(SystemExit) as pytest_wrapped_e:
		missedClassScrapper.MissedClassDates("16CSVWXYZ","password","2019-07-19")
	assert pytest_wrapped_e.type == SystemExit
	assert pytest_wrapped_e.value.code == 0