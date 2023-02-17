import maya.cmds as cmds
import sys, os
import yaml
import XLFACS.util.pathlib
import XLFACS.util.utility, pprint

YAML_STRUCTURE = r"C:\Users\jeffjung\Documents\maya\scripts\structure.yaml"
MAX_headJoint = "Bip001FBXASC032Head"



class CreateJoints():

	def __init__ ( self):

		global MAX_headJoint
		global YAML_STRUCTURE
		self.variable = []
		self.yaml_Path = YAML_STRUCTURE
		self.data_Structure = []

		# actual bind joints
		self.parent_Joints = []
		self.jaw_Joints = []
		self.nose_Joints = []
		self.mouth_Joints = []
		self.eyeL_Joints = []
		self.eyeR_Joints = []
		self.eyeBrowL_Joints = []
		self.eyeBrowR_Joints = []
		self.cheekL_Joints = []
		self.cheekR_Joints = []
		self.mouthLineL_Joints = []
		self.mouthLineR_Joints = []
		self.cheek_Joints = []
		self.eyeBallL_Joints = []
		self.eyeBallR_Joints = []
		self.eyeBrowC_Joints = []
		self.mouthUpside_Joints  = []
		self.jawEnd_Joints  = []
		self.setup()

	def setup( self):

		self.data_Structure = self.dataStructure()


		### parent joint
		self.parent_Joints = self.makeParentJoint( )

		### toughJaw structure
		jaw_Jnt = self.data_Structure[0]["jaw"]
		self.jaw_Joints = self.tongueJawCreate( jaw_Jnt, self.parent_Joints [0])
		self.jawConstrains( self.jaw_Joints)

		### nose structure
		nose_Jnt = self.data_Structure[0]["nose"]
		self.nose_Joints = self.noseCreate( nose_Jnt, self.parent_Joints [3])

		### mouth structure
		mouth_Jnt = self.data_Structure[0]["mouth"]
		mouth_Parent = mouth_Jnt["parent"]
		self.mouth_Joints = self.mouthCreate( mouth_Jnt, mouth_Parent)

		### eyeL structure
		eyeL_Jnt = self.data_Structure[0]["eyeL"]
		eyeL_Parent = eyeL_Jnt["parent"]
		self.eyeL_Joints = self.eyeLCreate( eyeL_Jnt, eyeL_Parent)

		### eyeR structure
		eyeR_Jnt = self.data_Structure[0]["eyeR"]
		eyeR_Parent = eyeR_Jnt["parent"]
		self.eyeR_Joints = self.eyeRCreate( eyeR_Jnt, eyeR_Parent)

		### eyeBrowC structure
		eyeBrowC_Jnt = self.data_Structure[0]["eyeBrowC"]
		eyeBrowC_Parent = eyeBrowC_Jnt["parent"]
		self.eyeBrowC_Joints = self.eyeBrowLCreate( eyeBrowC_Jnt, eyeBrowC_Parent)


		### eyeBrowL structure
		eyeBrowL_Jnt = self.data_Structure[0]["eyeBrowL"]
		eyeBrowL_Parent = eyeBrowL_Jnt["parent"]
		self.eyeBrowL_Joints = self.eyeBrowLCreate( eyeBrowL_Jnt, eyeBrowL_Parent)

		### eyeBrowR structure
		eyeBrowR_Jnt = self.data_Structure[0]["eyeBrowR"]
		eyeBrowR_Parent = eyeBrowR_Jnt["parent"]
		self.eyeBrowR_Joints = self.eyeBrowRCreate( eyeBrowR_Jnt, eyeBrowR_Parent)

		### cheekL structure
		cheekL_Jnt = self.data_Structure[0]["cheekL"]
		cheekL_Parent = cheekL_Jnt["parent"]
		self.cheekL_Joints = self.cheekLCreate( cheekL_Jnt, cheekL_Parent)

		### cheekR structure
		cheekR_Jnt = self.data_Structure[0]["cheekR"]
		cheekR_Parent = cheekR_Jnt["parent"]
		self.cheekR_Joints = self.cheekRCreate( cheekR_Jnt, cheekR_Parent)

		### mouthLineL structure
		mouthLineL_Jnt = self.data_Structure[0]["mouthLineL"]
		mouthLineL_Parent = mouthLineL_Jnt["parent"]
		self.mouthLineL_Joints = self.mouthLineLCreate( mouthLineL_Jnt, mouthLineL_Parent)

		### mouthLineR structure
		mouthLineR_Jnt = self.data_Structure[0]["mouthLineR"]
		mouthLineR_Parent = mouthLineR_Jnt["parent"]
		self.mouthLineR_Joints = self.mouthLineRCreate( mouthLineR_Jnt, mouthLineR_Parent)

		### cheek structure
		cheek_Jnt = self.data_Structure[0]["cheek"]
		cheek_Parent = cheek_Jnt["parent"]
		self.cheek_Joints = self.cheekCreate( cheek_Jnt, cheek_Parent)

		### eyeBallL structure
		eyeBallL_Jnt = self.data_Structure[0]["eyeBallL"]
		eyeBallL_Parent = eyeBallL_Jnt["parent"]
		self.eyeBallL_Joints = self.eyeBallLCreate( eyeBallL_Jnt, eyeBallL_Parent)

		### eyeBallR structure
		eyeBallR_Jnt = self.data_Structure[0]["eyeBallR"]
		eyeBallR_Parent = eyeBallR_Jnt["parent"]
		self.eyeBallR_Joints = self.eyeBallRCreate( eyeBallR_Jnt, eyeBallR_Parent)

		### mouthUpside
		mouthUp_Jnt = self.data_Structure[0]["mouthUpside"]
		mouthUp_Parent = mouthUp_Jnt["parent"]
		self.mouthUpside_Joints = self.mouthUpside( mouthUp_Jnt, mouthUp_Parent)


		### jawEnd
		jawEnd_Jnt = self.data_Structure[0]["jawEnd"]
		jawEndParent = jawEnd_Jnt["parent"]
		self.jawEnd_Joints = self.jawEnd( jawEnd_Jnt, jawEndParent)

		### parent facs_head to ori_head
		self.headParent( self.parent_Joints, MAX_headJoint)


	def makeJoints( self, yamlData):

		yamlData = yamlData
		keys = yamlData[1]  #
		values = yamlData[0]  #

		# make parent joints
		#
		#

		for i in keys:
			each_Joint =  values[i]["joints"]
			parent_Joint = values[i]["parent"]
			for j in each_Joint:
				pos_bone = FACS_utility.worldPosition( j)
				cmds.select( d=True)
				tempJoint = cmds.joint( p=pos_bone, zso=True, oj='xyz')
				cmds.select( d=True)
				cmds.parent( tempJoint, parent_Joint)

	#----------------------------------------------
	def dataStructure( self):
		dummy_Data = FACS_utility.yamlStructures( self.yaml_Path)
		dummy_Keys = dummy_Data.keys()
		return dummy_Data, dummy_Keys




	def eyeBallRCreate (self, eye_Joints, parent_Joint):

		eye_Joints = eye_Joints["joints"]
		parent_Joint = FACS_utility.prefixModifier( parent_Joint, strReplace="facs_", strRemove="D_")
		temp_Joints = []

		for i in eye_Joints:
			pos_parentJnt = FACS_utility.worldPosition( i)
			cmds.select( d=True)
			temp_Name = FACS_utility.prefixModifier( i, strReplace="facs_", strRemove="D_")
			tempJoint = cmds.joint( p=pos_parentJnt, n=temp_Name)
			cmds.select( d=True)
			temp_Joints.append( tempJoint)
			cmds.parent( tempJoint, parent_Joint)
		return temp_Joints

	def eyeBallLCreate (self, eye_Joints, parent_Joint):

		eye_Joints = eye_Joints["joints"]
		parent_Joint = FACS_utility.prefixModifier( parent_Joint, strReplace="facs_", strRemove="D_")
		temp_Joints = []

		for i in eye_Joints:
			pos_parentJnt = FACS_utility.worldPosition( i)
			cmds.select( d=True)
			temp_Name = FACS_utility.prefixModifier( i, strReplace="facs_", strRemove="D_")
			tempJoint = cmds.joint( p=pos_parentJnt, n=temp_Name)
			cmds.select( d=True)
			temp_Joints.append( tempJoint)
			cmds.parent( tempJoint, parent_Joint)
		return temp_Joints

	def cheekCreate (self, eye_Joints, parent_Joint):

		eye_Joints = eye_Joints["joints"]
		parent_Joint = FACS_utility.prefixModifier( parent_Joint, strReplace="facs_", strRemove="D_")
		temp_Joints = []

		for i in eye_Joints:
			pos_parentJnt = FACS_utility.worldPosition( i)
			cmds.select( d=True)
			temp_Name = FACS_utility.prefixModifier( i, strReplace="facs_", strRemove="D_")
			tempJoint = cmds.joint( p=pos_parentJnt, n=temp_Name)
			cmds.select( d=True)
			temp_Joints.append( tempJoint)
			cmds.parent( tempJoint, parent_Joint)
		return temp_Joints

	def mouthLineRCreate (self, eye_Joints, parent_Joint):

		eye_Joints = eye_Joints["joints"]
		parent_Joint = FACS_utility.prefixModifier( parent_Joint, strReplace="facs_", strRemove="D_")
		temp_Joints = []

		for i in eye_Joints:
			pos_parentJnt = FACS_utility.worldPosition( i)
			cmds.select( d=True)
			temp_Name = FACS_utility.prefixModifier( i, strReplace="facs_", strRemove="D_")
			tempJoint = cmds.joint( p=pos_parentJnt, n=temp_Name)
			cmds.select( d=True)
			temp_Joints.append( tempJoint)
			cmds.parent( tempJoint, parent_Joint)
		return temp_Joints

	def mouthLineLCreate (self, eye_Joints, parent_Joint):

		eye_Joints = eye_Joints["joints"]
		parent_Joint = FACS_utility.prefixModifier( parent_Joint, strReplace="facs_", strRemove="D_")
		temp_Joints = []

		for i in eye_Joints:
			pos_parentJnt = FACS_utility.worldPosition( i)
			cmds.select( d=True)
			temp_Name = FACS_utility.prefixModifier( i, strReplace="facs_", strRemove="D_")
			tempJoint = cmds.joint( p=pos_parentJnt, n=temp_Name)
			cmds.select( d=True)
			temp_Joints.append( tempJoint)
			cmds.parent( tempJoint, parent_Joint)
		return temp_Joints

	def cheekRCreate (self, eye_Joints, parent_Joint):

		eye_Joints = eye_Joints["joints"]
		parent_Joint = FACS_utility.prefixModifier( parent_Joint, strReplace="facs_", strRemove="D_")
		temp_Joints = []

		for i in eye_Joints:
			pos_parentJnt = FACS_utility.worldPosition( i)
			cmds.select( d=True)
			temp_Name = FACS_utility.prefixModifier( i, strReplace="facs_", strRemove="D_")
			tempJoint = cmds.joint( p=pos_parentJnt, n=temp_Name)
			cmds.select( d=True)
			temp_Joints.append( tempJoint)
			cmds.parent( tempJoint, parent_Joint)
		return temp_Joints

	def cheekLCreate (self, eye_Joints, parent_Joint):

		eye_Joints = eye_Joints["joints"]
		parent_Joint = FACS_utility.prefixModifier( parent_Joint, strReplace="facs_", strRemove="D_")
		temp_Joints = []

		for i in eye_Joints:
			pos_parentJnt = FACS_utility.worldPosition( i)
			cmds.select( d=True)
			temp_Name = FACS_utility.prefixModifier( i, strReplace="facs_", strRemove="D_")
			tempJoint = cmds.joint( p=pos_parentJnt, n=temp_Name)
			cmds.select( d=True)
			temp_Joints.append( tempJoint)
			cmds.parent( tempJoint, parent_Joint)
		return temp_Joints



	def eyeBrowCCreate (self, eye_Joints, parent_Joint):

		eye_Joints = eye_Joints["joints"]
		parent_Joint = FACS_utility.prefixModifier( parent_Joint, strReplace="facs_", strRemove="D_")
		temp_Joints = []

		for i in eye_Joints:
			pos_parentJnt = FACS_utility.worldPosition( i)
			cmds.select( d=True)
			temp_Name = FACS_utility.prefixModifier( i, strReplace="facs_", strRemove="D_")
			tempJoint = cmds.joint( p=pos_parentJnt, n=temp_Name)
			cmds.select( d=True)
			temp_Joints.append( tempJoint)
			cmds.parent( tempJoint, parent_Joint)
		return temp_Joints


	def eyeBrowRCreate (self, eye_Joints, parent_Joint):

		eye_Joints = eye_Joints["joints"]
		parent_Joint = FACS_utility.prefixModifier( parent_Joint, strReplace="facs_", strRemove="D_")
		temp_Joints = []

		for i in eye_Joints:
			pos_parentJnt = FACS_utility.worldPosition( i)
			cmds.select( d=True)
			temp_Name = FACS_utility.prefixModifier( i, strReplace="facs_", strRemove="D_")
			tempJoint = cmds.joint( p=pos_parentJnt, n=temp_Name)
			cmds.select( d=True)
			temp_Joints.append( tempJoint)
			cmds.parent( tempJoint, parent_Joint)
		return temp_Joints

	def eyeBrowLCreate (self, eye_Joints, parent_Joint):

		eye_Joints = eye_Joints["joints"]
		parent_Joint = FACS_utility.prefixModifier( parent_Joint, strReplace="facs_", strRemove="D_")
		temp_Joints = []

		for i in eye_Joints:
			pos_parentJnt = FACS_utility.worldPosition( i)
			cmds.select( d=True)
			temp_Name = FACS_utility.prefixModifier( i, strReplace="facs_", strRemove="D_")
			tempJoint = cmds.joint( p=pos_parentJnt, n=temp_Name)
			cmds.select( d=True)
			temp_Joints.append( tempJoint)
			cmds.parent( tempJoint, parent_Joint)
		return temp_Joints

	def eyeLCreate (self, eye_Joints, parent_Joint):

		eye_Joints = eye_Joints["joints"]
		parent_Joint = FACS_utility.prefixModifier( parent_Joint, strReplace="facs_", strRemove="D_")
		temp_Joints = []

		for i in eye_Joints:
			pos_parentJnt = FACS_utility.worldPosition( i)
			cmds.select( d=True)
			temp_Name = FACS_utility.prefixModifier( i, strReplace="facs_", strRemove="D_")
			tempJoint = cmds.joint( p=pos_parentJnt, n=temp_Name)
			cmds.select( d=True)
			temp_Joints.append( tempJoint)
			cmds.parent( tempJoint, parent_Joint)
		return temp_Joints

	def eyeRCreate (self, eye_Joints, parent_Joint):

		eye_Joints = eye_Joints["joints"]
		parent_Joint = FACS_utility.prefixModifier( parent_Joint, strReplace="facs_", strRemove="D_")
		temp_Joints = []

		for i in eye_Joints:
			pos_parentJnt = FACS_utility.worldPosition( i)
			cmds.select( d=True)
			temp_Name = FACS_utility.prefixModifier( i, strReplace="facs_", strRemove="D_")
			tempJoint = cmds.joint( p=pos_parentJnt, n=temp_Name)
			cmds.select( d=True)
			temp_Joints.append( tempJoint)
			cmds.parent( tempJoint, parent_Joint)
		return temp_Joints

	def mouthCreate (self, mouth_Joints, parent_Joint):

		mouth_Joints = mouth_Joints["joints"]
		parent_Joint = FACS_utility.prefixModifier( parent_Joint, strReplace="facs_", strRemove="D_")
		temp_Joints = []

		for i in mouth_Joints:
			pos_parentJnt = FACS_utility.worldPosition( i)
			cmds.select( d=True)
			temp_Name = FACS_utility.prefixModifier( i, strReplace="facs_", strRemove="D_")
			tempJoint = cmds.joint( p=pos_parentJnt, n=temp_Name)
			cmds.select( d=True)
			temp_Joints.append( tempJoint)
			cmds.parent( tempJoint, parent_Joint)
		return temp_Joints

	def noseCreate (self, nose_Joints, parent_Joint):

		nose_Joints = nose_Joints["joints"]
		parent_Joint = parent_Joint
		temp_Joints = []


		for i in nose_Joints:
			pos_parentJnt = FACS_utility.worldPosition( i)
			cmds.select( d=True)
			temp_Name = FACS_utility.prefixModifier( i, strReplace="facs_", strRemove="D_")
			tempJoint = cmds.joint( p=pos_parentJnt, n=temp_Name)
			cmds.select( d=True)
			temp_Joints.append( tempJoint)
			cmds.parent( tempJoint, parent_Joint)

		return temp_Joints



	def mouthUpside (self, mouthUpside, parent_Joint):

		mouthUpside = mouthUpside["joints"]

		parent_Joint = FACS_utility.prefixModifier( parent_Joint, strReplace="facs_", strRemove="D_")
		temp_Joints = []

		for i in mouthUpside:
			pos_parentJnt = FACS_utility.worldPosition( i)
			cmds.select( d=True)
			temp_Name = FACS_utility.prefixModifier( i, strReplace="facs_", strRemove="D_")
			tempJoint = cmds.joint( p=pos_parentJnt, n=temp_Name)
			cmds.select( d=True)
			temp_Joints.append( tempJoint)
			cmds.parent( tempJoint, parent_Joint)
		return temp_Joints


	def jawEnd (self, jawEnd, parent_Joint):

		jawEnd = jawEnd["joints"]

		parent_Joint = FACS_utility.prefixModifier( parent_Joint, strReplace="facs_", strRemove="D_")
		temp_Joints = []

		for i in jawEnd:
			pos_parentJnt = FACS_utility.worldPosition( i)
			cmds.select( d=True)
			temp_Name = FACS_utility.prefixModifier( i, strReplace="facs_", strRemove="D_")
			tempJoint = cmds.joint( p=pos_parentJnt, n=temp_Name)
			cmds.select( d=True)
			temp_Joints.append( tempJoint)
			cmds.parent( tempJoint, parent_Joint)
		return temp_Joints



	def makeParentJoint( self):
		temp_Joints = []

		head_Joint = ["D_head"]
		pos_parentJnt = FACS_utility.worldPosition( head_Joint)
		cmds.select( d=True)
		temp_Name = FACS_utility.prefixModifier( head_Joint[0], strReplace="facs_", strRemove="D_")
		tempJoint = cmds.joint( p=pos_parentJnt, n=temp_Name)
		temp_Joints.append( tempJoint)
		cmds.select( d=True)

		parent_Joints = ["D_eyeBallL", "D_eyeBallR", "D_nose"]
		for i in parent_Joints:
			pos_parentJnt = FACS_utility.worldPosition( i)
			cmds.select( d=True)
			temp_Name = FACS_utility.prefixModifier( i, strReplace="facs_", strRemove="D_")
			tempJoint = cmds.joint( p=pos_parentJnt, n=temp_Name + "_G")
			cmds.select( d=True)
			temp_Joints.append( tempJoint)
			cmds.parent( tempJoint, temp_Joints[0])

		return temp_Joints

	# parent joint function needed
	def tongueJawCreate( self, jaw_Joints, parent_Joint):

		# print jaw_Joints["joints"]
		each_Joint = jaw_Joints["joints"]
		parent_Joint = parent_Joint
		tongueJaw_Joint = []
		temp_jaw_G = []
		temp_jaw = []

		### tough structure
		for j in each_Joint:
			pos_bone = FACS_utility.worldPosition( j)
			cmds.select( d=True)
			temp_Name = FACS_utility.prefixModifier( j, strReplace="facs_", strRemove="D_")

			if "jaw" in temp_Name:
				temp_jaw = temp_Name
				temp_Name = temp_Name + "_G"
				temp_jaw_G = temp_Name

			tempJoint = cmds.joint( p=pos_bone, n=temp_Name)
			tongueJaw_Joint.append( tempJoint)
			cmds.select( d=True)

		# parent tough joints
		for i in tongueJaw_Joint[:-1]:
			index_num = tongueJaw_Joint.index(i)
			cmds.parent( i, tongueJaw_Joint[index_num + 1])

		# orient joint
		# cmds.joint( tongueJaw_Joint[-1], e=1, oj="xyz", secondaryAxisOrient="yup", ch=1, zso=1)
		cmds.joint( tongueJaw_Joint[-1], e=1,oj="none", ch=0, zso=1)
		cmds.joint( tongueJaw_Joint[0], e=1,oj="none", ch=1, zso=1)


		### jaw structure
		jaw_G_orientY = cmds.getAttr( temp_jaw_G + ".jointOrientY")
		cmds.select( d=True)
		pos_bone = FACS_utility.worldPosition( temp_jaw_G)
		tempJoint = cmds.joint( p=pos_bone, n=temp_jaw)
		cmds.setAttr( tempJoint + ".jointOrientY", jaw_G_orientY)
		cmds.select( d=True)

		tongueJaw_Joint.append( temp_jaw)

		cmds.parent( temp_jaw_G, parent_Joint)
		cmds.parent( temp_jaw, parent_Joint)

		return tongueJaw_Joint

	def jawConstrains( self, jaw_Jnt):

		constrain_Jnt = jaw_Jnt
		jaw_constraints = []
		jaw_constraints.append( cmds.parentConstraint( constrain_Jnt[-1], constrain_Jnt[-2], n='jaw_p_constrain'))
		jaw_constraints.append( cmds.scaleConstraint ( constrain_Jnt[-1], constrain_Jnt[-2], n='jaw_s_constrain'))
		return jaw_constraints

	def headParent( self, parent_facs, parent_head):

		parent_facs = parent_facs
		parent_head = MAX_headJoint
		constraint_head = []

		if cmds.objExists(parent_head):
			constraint_head = cmds.connectJoint( parent_facs[0], parent_head, pm=True )

		return constraint_head

ffa = CreateJoints()






