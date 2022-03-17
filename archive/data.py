import os, sys
import re
import shutil

re_han = re.compile("([\u4E00-\u9FD5a-zA-Z0-9+#&\._%\-]+)", re.U)
re_skip = re.compile("(\r\n|\s)", re.U)

type_dict={}
def fetch_type(filename):
    with open(os.path.join(os.getcwd(), filename), mode="r+", encoding="utf-8") as r:
        lines = r.readlines()
    for i in range (1, len(lines)):
        blocks = re_han.split(lines[i])
        name = ""
        types = []
        for blk in blocks:
            if not blk:
                continue
            if re_han.match(blk):
                if name == "":
                    name = blk
                else:
                    types.append(blk)
        
        for type_ in types:
            type_dict.setdefault(type_,[]).append(name)

def sort_data(src_path, dst_path):
    for type_ in type_dict:
        type_dir_path = dst_path + str(type_)
        if not os.path.exists(type_dir_path):
            os.system("mkdir " + type_dir_path)
        for pokemon in type_dict[type_]:
            pokemon_image_path = src_path + str(pokemon) + ".png"
            if not os.path.exists(pokemon_image_path):
                pokemon_image_path = src_path + str(pokemon) + ".jpg"
            # print(pokemon_image_path)
            # print(os.path.exists(pokemon_image_path))
            shutil.copyfile(pokemon_image_path, type_dir_path + "/" + str(pokemon) + ".png")
        

fetch_type("pokemon.csv")
# for type_ in type_dict:
#     print(str(type_) + ":\n" + str(type_dict[type_]))
sort_data("./images/images/", "./sorted_images/")
#shutil.copyfile("./images/images/abomasnow.png", "./sorted_images/Bug/abomasnow.png")