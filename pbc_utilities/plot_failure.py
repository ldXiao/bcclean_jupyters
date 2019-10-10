import igl
import meshplot as mp
import numpy as np
import yaml
import os
from enum import Enum


def CC_faces_per_node(v:np.array, f:np.array, node_list:np.array):
    """
    v: vertices list
    f: faces list
    node_list is a list of vertices index which are presumbly NNodes
    """
    node_face_dict = {}
    vf, ni=igl.vertex_triangle_adjacency(f, len(v))
    print("adjacency detcted")
    for nd in node_list:
        nd_f_num = ni[nd+1]-ni[nd] # number of faces adjacent to nd
        node_face_dict[nd] = []
        pool = [vf[ni[nd]+j] for j in range(nd_f_num)]
        head = pool.pop()
        node_face_dict[nd].append(head)
        while pool:
            fidx = node_face_dict[nd][-1]
            fi_list = f[fidx]
            nd_idx = 0
            for j, vidx in enumerate(fi_list):
                if vidx == nd:
                    nd_idx = j
                    break
            fi_list=np.delete(fi_list, (nd_idx+1) % 3,0)
            #compare with the last face index in target dictionary
            find = False
            for k in range(len(pool)):
                fkdx = pool[k]
                fk_list = f[fkdx]
                intersection = [val for val in fi_list if val in fk_list]

                if(len(intersection)==2):
#                     print(fi_list, fk_list)
                    popk=pool.pop(k)
                    node_face_dict[nd].append(popk)
                    find = True
                    break
                else:
                    find = False
            if(find==False):
                return None
    return node_face_dict

def get_feat_file(parent_dir):
    for file in os.listdir(parent_dir):
        if ".yml" in file:
#             print(os.path.join(parent_dir, file))
            return os.path.join(parent_dir, file)
    return None

def parse_feat(in_feat_file_name, out_file_body="feat"):
    parent_dir = os.path.dirname(in_feat_file_name)
    out_file_name = out_file_body+".dmat"
    out_file_rel_dir = os.path.join(parent_dir, out_file_name)
        # return the file path if the output file already exists
    with open(in_feat_file_name, 'r') as stream:
        try:
            yaml_dict=yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    face_label_dict = {}
    count =0
    for label, surface in enumerate(yaml_dict["surfaces"]):
        for face_id in surface["face_indices"]:
            face_label_dict[face_id] = label
            count +=1
    with open(out_file_rel_dir, 'w') as f:
        f.write("1"+" "+str(count)+"\n")
        for item in sorted(face_label_dict.keys()):
            f.write("%s\n" % face_label_dict[item])
    return out_file_rel_dir

def get_bad_mesh(parent_dir):
    for file in os.listdir(parent_dir):
        if (file[-4:]==".obj"):
            if file[-8:]=="__sf.obj" or file=="good_mesh.obj":
                continue
            else:
                return os.path.join(parent_dir, file)
    return None

def build_adj_dict(edge_list, label_num):
    pair_edge_dict = {}
    adj_matrix = np.zeros((label_num, label_num), dtype="int32")
    for i,edg in enumerate(edge_list):
        x, y = edg.label_pair
        adj_matrix[x,y]+= 1
        if (x,y) not in pair_edge_dict:
            pair_edge_dict[(x,y)]= [i]
        else:
            pair_edge_dict[(x,y)].append(i)
    return pair_edge_dict, adj_matrix

def extract_patches(V, F, FL):
    '''
    return patch_dict {label_i: (V_i, F_i, I_i, J_i)}
    '''
    label_num = FL.max()+1
    patch_idx_dict = {}
    for fidx, fl in enumerate(FL):
        if fl not in patch_idx_dict:
            patch_idx_dict[fl] = [fidx]
        else:
            patch_idx_dict[fl].append(fidx)
    patch_dict = {}
    for key in patch_idx_dict:
        F_key = F[patch_idx_dict[key]]
        V_key, F_key, I_key, J_key = igl.remove_unreferenced(V, F_key)
        patch_dict[key] = (V_key, F_key, I_key, J_key)
    return patch_dict


def union_meshes(V0, F0, V1, F1):
    vnum0 = len(V0)
    offset  = np.ones_like(F1) * vnum0
    Vr=np.vstack([V0, V1])
    Fr = np.vstack([F0, F1+offset])
    return Vr,Fr

class bdtype(Enum):
    NODE = 0
    EDGE = 1

class loop():
    _label = 0
    _loop_list = []
    

