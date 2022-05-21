import yaml, sys, os
import maya.cmds as cmds


############# utilities for generating skeleton #############

def yamlStructures( filePath):
	'''
	read yaml config file for facial structure

	CONF_FILE = r"F:/artwork/99_pipeline/Coding/xlgames/xlfacs/xlFACS/structure.yaml"
	structures = yamlStructures( CONF_FILE)
	all_keys = structures.keys()

	'''
	print "asdfasdfas"
	# variables
	corret_path = os.path.normpath( filePath)
	# corret_path = filePath

	#print corret_path

	# get structure from yaml
	try:
		with open( corret_path) as f:
		    conf_file = yaml.load( f, Loader=yaml.FullLoader)
		    ch_parts = conf_file.get( "facialGrp")
		return ch_parts
	except:
		print "there is no file"


def worldPosition( inputObject):
	'''
	get world position data
	'''
	wPosition = cmds.xform(inputObject, t=True , q=True , ws=True, a=True)
	return wPosition



def prefixModifier( stringObject, strReplace=None, strRemove=None):
	'''
	Prefix change or remove function

    :param
    :return
	
	-> prefixModifier( "D_eyeL_DDD_D", strReplace="facial_", strRemove="D_")
	'''

	# variables
	post_name = stringObject
	pre_prefix = strRemove
	post_prefix = strReplace
	new_name = []


	if isinstance( post_name, str):
		pass
	elif isinstance( post_name, list):
		post_prefix = str( post_prefix)

	# 
	if pre_prefix != None and post_prefix == None:
		new_name = post_name.split( pre_prefix)[1]
	elif pre_prefix != None and post_prefix != None:
	    new_name = post_name.replace( pre_prefix, post_prefix)
	else:
		new_name = post_name.split("_", 1)[1]

	return new_name


CONF_FILE = r"C:\\Users\\jeffjung\\Documents\\maya\\2022\\scripts\\structure.yaml"
structures = yamlStructures( CONF_FILE)
all_keys = structures.keys()
