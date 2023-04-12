# %%
from preprocessor.facealign_preprocessor import facealign_preprocessor
from requestbody.AlignFaceRequestBody import AlignFaceRequestBody
from requestbody.CombineAvatarRequestBody import CombinAvatarRequestBody
from requestbody.MakeHeadRequestItem import MakeHeadRequestItem
import tempfile
from fastapi import FastAPI, Depends
import requests
import os, sys
from repository.mysql_repository import mysql_repository
from responsebody.MakeHeadResponseItem import MakeHeadResponseItem
from storage.web_storage import web_storage
import uvicorn
import time
def add_system_path_my_avatar_ai():
    sys.path.insert(0, os.path.join(os.getcwd(), 'my_avatar_ai'))

add_system_path_my_avatar_ai()

def get_temp_dir():
    dir = tempfile.TemporaryDirectory()
    try:
        yield dir.name
    finally:
        del dir

from my_avatar_ai.infer import Model2D, Model3D
app = FastAPI()
repositoy = mysql_repository()
storage = web_storage()
preprocessor = facealign_preprocessor()

model2D = Model2D("my_avatar_ai/CartoonStyleGAN/networks")
model3D = Model3D()


@app.post("/make-head", response_model=MakeHeadResponseItem)
def make_head(item : MakeHeadRequestItem, dir=Depends(get_temp_dir)):
    photo_dir = dir + "/photo"
    cartoon_dir = dir + "/cartoon"
    avatar_dir = dir + "/avatar"
    os.mkdir(photo_dir)
    os.mkdir(cartoon_dir)
    os.mkdir(avatar_dir)
    
    file, ext = os.path.splitext(item.photo_url)
    photo_fullpath = photo_dir + '/usr_photo' + ext
    storage.file_download(photo_fullpath, item.photo_url)
    
    model2D.inference(input_path = photo_fullpath,
                      output_path = cartoon_dir + "/",
                      make_all = False,
                      style = item.style_code)
    
    model3D.inference(input_path = cartoon_dir,
                      output_path = avatar_dir,
                      get_full = True)
    
    # cartoon화된 이미지 갖고 오기
    toonify_list = os.listdir(cartoon_dir)
    try :
        toonify_img = cartoon_dir + '/' + toonify_list[0]
    except :
        raise ValueError
    # fbx 만들어서 받기
    file_basename = 'usr_photo-align-{}'.format(item.style_code)
    obj_dir = avatar_dir + '/' + file_basename
    mtl_file = open(obj_dir + '/{}.mtl'.format(file_basename), 'rb')
    obj_file = open(obj_dir + '/{}.obj'.format(file_basename), 'rb')
    png_file = open(obj_dir + '/{}.png'.format(file_basename), 'rb')
    normal_file = open(obj_dir + '/{}_normals.png'.format(file_basename), 'rb')
    response = requests.post("https://myavatar.co.kr/fbx/obj2fbx",
                  files={'mtl' : mtl_file, 'obj' : obj_file, 'png' : png_file, 'normal' : normal_file}, data={'name' : file_basename})
    head_fbx = '{}/{}.fbx'.format(dir, 'avatar')
    with open(head_fbx, "wb") as file:
        file.write(response.content)
    
    # 결과 전송
    toonify_url = storage.file_upload(toonify_img)
    head_url = storage.file_upload(head_fbx)
    
    return MakeHeadResponseItem(toonify_url=toonify_url, head_url=head_url, result=0)
    
@app.post("/align_face")
def align_face(item : AlignFaceRequestBody):
    return_url : str
    with tempfile.TemporaryDirectory() as dir:
        file, ext = os.path.splitext(item.photo_url)
        photo_fullpath = "{}/{}{}".format(dir, 'photo', ext)
        storage.file_download(photo_fullpath, item.photo_url)
        photo_fullpath = preprocessor.preprocess(photo_fullpath)
        return_url = storage.file_upload(photo_fullpath)
    
    if return_url:
        return {'photoUrl': return_url}
    else:
        raise ValueError
    
@app.post("/combine-avatar")
def combine_avatar(item : CombinAvatarRequestBody, dir=Depends(get_temp_dir)):
    body_config = repositoy.get_body_config(item.body_num)
    hair_config = repositoy.get_hair_config(item.hair_num)
    body_url = repositoy.get_body_url(item.body_num)
    hair_url = repositoy.get_hair_url(item.hair_num)
    body_value = {'head_url' : item.head_url,
                  'body_url' : body_url,
                  'hair_url' : hair_url,
                  'body_config' : body_config,
                  'hair_config' : hair_config}
    print(body_value)
    response = requests.post('https://myavatar.co.kr/fbx/merge-full-fbx', json = body_value)
    result = {'objectUrl' : None, 'result' : 0}
    fullfbx = dir + '/fullAvatar.fbx'
    with open(fullfbx, 'wb') as fbxfile:
        fbxfile.write(response.content)
    result['objectUrl'] = storage.file_upload(fullfbx)
    return result
    
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1010)