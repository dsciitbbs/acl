import pytest
from mockito import ANY, when, mock, unstub
import sys
import os
sys.path.insert(0, os.getcwd())
from source import scrapper

def test_attempt():

	with open("res/erp_standard.html") as f:
		text = f.read()

	when(scrapper).network(...).thenReturn(text)
	table = scrapper.attempt("16CSVWXYZ","password")
	
	assert len(table), 7
	assert table.keys(), ["CS4L001","CS4P001","CS4T001","CS4D001","CS6L029","CS6L002","CS6L010"]

	unstub()

def test_attempt_none():

	when(scrapper).network(...).thenReturn(None)
	table = scrapper.attempt("16CSVWXYZ","password")
	
	assert not table

	unstub()

def test_network_error():
	
	with pytest.raises(SystemExit) as pytest_wrapped_e:
		scrapper.network("16CSVWXYZ","password","abc.xyz.com")
	assert pytest_wrapped_e.type == SystemExit
	assert pytest_wrapped_e.value.code == 0
