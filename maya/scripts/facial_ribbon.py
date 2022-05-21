# Utilities
from maya import cmds
import maya.api.OpenMaya as om
import operator
import maya.mel as mel
### Findout Closest Vertex


joint_ob = ['facs_eyeDnR_01','facs_eyeDnR_02','facs_eyeDnR_03']
fol_ob = ['eyelipDnR_surfaceFollicle50', 'eyelipDnR_surfaceFollicle5050', 'eyelipDnR_surfaceFollicle9950']
origin_mesh = 'Nu_M_BaseBody_Face01'
ribbon_mesh = 'eyelipDnR_surface'

class ribbon:

    def __init__(self, origin_mesh, joint_object, fol_object, ribbon_mesh):
   
        self.joints_ob = joint_object
        self.fol_ob = fol_object
        self.origon_mesh = origin_mesh
        self.ribbon_mesh = ribbon_mesh


        # first setup
        # skin
        # transform connection
        self.target_con = []
        self.first_setup()

        # skin joint to loft mesh
        skin_joint = []
        for i, j in self.target_con:
            skin_joint.append( j)

        skin_cluster = cmds.skinCluster(skin_joint, ribbon_mesh, name='spine_skinCluster', toSelectedBones=True, bindMethod=0, skinMethod=0, normalizeWeights=1)[0]
        self.constrain_joint( self.joints_ob, self.fol_ob)

        # second setup
        self.target_five_con = []
        self.second_setup()
        self.second_organize(self.target_con, self.target_five_con)


    def second_organize( self, source, target):


        #cmds.shadingNode('multiplyDivide', asUtility=True, name='multiplyDivideTest')
        #cmds.connectAttr(src_text_value + ".translate", trg_text_value + ".translate")

        rivet_group = []


        for (i, j) in enumerate( target):

            multi_node = cmds.shadingNode('multiplyDivide', asUtility=True)
            cmds.setAttr( multi_node+".input2X", -1)
            cmds.setAttr( multi_node+".input2Y", -1)
            cmds.setAttr( multi_node+".input2Z", -1)

            cmds.connectAttr( j[0]+".translate", multi_node+".input1")
            cmds.connectAttr( multi_node+".output", j[1]+".translate")
            cmds.connectAttr( j[0]+".translate", source[i][0]+".translate")
            cmds.connectAttr( j[0]+".rotate", source[i][0]+".rotate")
           
            rivet_temp = self.makeFolicleConstrain( self.origon_mesh, j[0])
            rivet_group.append( rivet_temp)
           
            cmds.pointConstraint( rivet_temp, j[1], maintainOffset=True, weight=1)
           
        cmds.group( rivet_group, n="rivet_follow")




    def first_setup( self):
        for i in self.joints_ob:
            ws = self.worldPosition( i)
            temp = self.fifth_jt_group( i, position=ws)
            self.target_con.append( temp)

   
    def second_setup( self):
        for j in self.joints_ob:
            ws = self.worldPosition( j)
            temp = self.fifth_group( j, position=ws)
            self.target_five_con.append( temp)


    def constrain_joint( self, target, source):
        for i, j in zip(source, target):
            cmds.pointConstraint( i, j, maintainOffset=True, weight=1)
            cmds.orientConstraint( i, j, maintainOffset=True, weight=1)


    def first_setup(self):
        for i in self.joints_ob:
            ws = self.worldPosition( i)
            temp = self.fifth_jt_group( i, position=ws)
            self.target_con.append( temp)


    def worldPosition( self, inputObject):
        '''
        get world position data
        '''
        wPosition = cmds.xform(inputObject, t=True , q=True , ws=True, a=True)
        return wPosition


    def fifth_jt_group( self, objectMesh, position=[0,0,0]):
        if isinstance( objectMesh, list):
            objectMesh = objectMesh[0]

        cmds.select(d =1)
        cr_joint = cmds.joint( n= (objectMesh + "_ctl_jt"))
        cmds.select(d =1)

        direction = ['v', 'w', 'x', 'y', 'z']

        temp= []
        last_group = []
        cmds.select(cr_joint)
        for i in direction:
            last_group = cmds.group( n= objectMesh + "_grp_jt_" + i)
            temp.append( last_group)
            cmds.select( last_group)
        cmds.xform( last_group, t=position, ws=1, a=1)
   
        return (temp[3], cr_joint)


    def getClosestVertex( self, mesh, guide):
        """Return closest vertex and distance from mesh to world-space position [x, y, z].
           
        Uses om.MfnMesh.getClosestPoint() returned face ID and iterates through face's vertices.
       
        Example:
            >>> getClosestVertex("pCube1", "locator1")
            # (3, 0.0)
            >>> getClosestVertex("pCube1", "locator1")
            # (3, 0.4)
   
        Args:
            mesh (str): Mesh node name.
            pos (list): Position vector XYZ
           
        Returns:
            tuple: (vertex index, distance)
       
        """
        pos = om.MPoint( cmds.xform( guide, q=1, t=1, ws=1, a=1))
        sel = om.MSelectionList()
        sel.add(mesh)
        fn_mesh = om.MFnMesh(sel.getDagPath(0))
       
        index = fn_mesh.getClosestPoint(pos, space=om.MSpace.kWorld)[1]  # closest polygon index    
        face_vertices = fn_mesh.getPolygonVertices(index)  # get polygon vertices
       
        vertex_distances = ((vertex, fn_mesh.getPoint(vertex, om.MSpace.kWorld).distanceTo(pos))
                             for vertex in face_vertices)
        return min(vertex_distances, key=operator.itemgetter(1))

    def worldPosition( self, inputObject):
        '''
        get world position data
        '''
        wPosition = cmds.xform(inputObject, t=True , q=True , ws=True, a=True)
        return wPosition


    def fifth_group( self, objectName, position=[0,0,0]):
   
        objectMesh = []
   
        if isinstance( objectName, list):
            objectName = objectName[0]
   
        objectMesh.append( cmds.sphere( n=objectName + "_ctl", ch=0, r=0.25))
        direction = ['v', 'w', 'x', 'y', 'z']
        cmds.select( objectMesh[0])
   
   
        if isinstance(objectMesh, list):
            objectMesh = objectMesh[0]
   
        last_group = []
        for i in direction:
            last_group = cmds.group( n=objectName + "_ctl_grp_" + i)
            objectMesh.append( last_group)
            cmds.select( last_group)
        cmds.xform( last_group, t=position, ws=1, a=1)
   
        return objectMesh

    def makeFolicleConstrain(self, baseMesh, targetMesh):
        '''
        targetMesh has to have five groups
        '''
   
        if isinstance(baseMesh, list):
            baseMesh = baseMesh[0]
   

        closeVex = self.getClosestVertex( baseMesh, targetMesh)
       
        cmds.select( baseMesh + ".vtx[" + str( closeVex[0]) + "]")
        rivet_out = mel.eval(  "Rivet;")
        rivet_name = cmds.ls(sl=1)[1]
        cmds.select( rivet_name)
        rivet_name = cmds.rename( targetMesh + "_follow")
        cmds.select( d=1)
        # vtx_pos = cmds.xform( baseMesh + ".vtx[" + str( closeVex[0]) + "]", q=1, t=1, ws=1, a=1)
        return rivet_name




ribbon( origin_mesh, joint_ob, fol_ob, ribbon_mesh)