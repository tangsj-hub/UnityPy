#!/Users/Jesli/opt/anaconda3/bin/python
# -*- coding: UTF-8 -*-

import io, os
import UnityPy
import sys, getopt
import traceback
import json
from PIL import Image
import imageio

class UnpackAutoEmote:
    def __init__(self, inFile, outDir):
        self.inFile = inFile
        self.outDir = outDir

    def GetOutDirByType(self, typeName):
        return os.path.join(self.outDir, typeName)

    def resize_and_center_crop(self, image_path, output_path, size=(500, 500)):
        # 打开原始图片
        original_image = Image.open(image_path)
        
        # 获取原始图片的宽度和高度
        width, height = original_image.size
        
        # 创建一个新的 500x500 的透明图片
        new_image = Image.new('RGBA', size, (0, 0, 0, 0))  # 透明背景
        
        # 计算居中位置
        x_offset = (size[0] - width) // 2
        y_offset = (size[1] - height) // 2
        
        # 将原始图片居中放置在新图片中
        new_image.paste(original_image, (x_offset, y_offset))
        
        # 保存新的图片
        new_image.save(output_path)
    def split_and_create_gif(self, image_path, output_path, img_name):
        # 打开原始图片
        original_image = Image.open(image_path)
        width, height = original_image.size
        w2, h2 = width // 2, height // 2

        # 按照 1（上左）、2（上右）、3（下左）、4（下右）顺序切割
        frame1 = original_image.crop((0, 0, w2, h2))         # 上左
        frame2 = original_image.crop((w2, 0, width, h2))     # 上右
        frame3 = original_image.crop((0, h2, w2, height))    # 下左
        frame4 = original_image.crop((w2, h2, width, height))# 下右

        # 可选：保存每一帧图片
        targetDir_k = self.GetOutDirByType('Texture2D-k')
        frame1.save(f"{targetDir_k}/{img_name}_1.png")
        frame2.save(f"{targetDir_k}/{img_name}_2.png")
        frame3.save(f"{targetDir_k}/{img_name}_3.png")
        frame4.save(f"{targetDir_k}/{img_name}_4.png")

        # 统一尺寸
        size = (256, 256)
        frames = []
        for frame in [frame1, frame2, frame3, frame4]:
            resized = frame.resize(size)
            bg = Image.new('RGBA', size, (0, 0, 0, 0))
            bg.paste(resized, (0, 0))
            frames.append(bg)

        # 合成 GIF
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=120,  # 可调整
            loop=0
        )
    def split_image_to_gif(self, image_path, gif_path, frame_duration = 1):
        # 打开图片
        img = Image.open(image_path)
        
        # 获取图片的宽和高
        width, height = img.size
        
        # 计算每个子图的宽和高
        mid_width = width // 2
        mid_height = height // 2

        # 分割图片
        top_left = img.crop((0, 0, mid_width, mid_height))
        top_right = img.crop((mid_width, 0, width, mid_height))
        bottom_left = img.crop((0, mid_height, mid_width, height))
        bottom_right = img.crop((mid_width, mid_height, width, height))

        # size = (256, 256)
        # background = Image.new('RGBA', size, (0, 0, 0, 0))  # 透明背景
        # 创建一个列表存储每一帧
        frames = [bottom_right, top_left, top_right, bottom_left, bottom_right]
        # 保存为GIF
        # 设置每一帧的持续时间
        imageio.mimsave(gif_path, frames, 'GIF', duration=frame_duration, loop=0)

        print(f"GIF已保存为: {gif_path}")
    
    # 切割默认表情图片
    # 输入图片路径和输出文件名前缀
    def split_Default_Emotes_image(self, image_path, output_prefix):
        try:
            # 打开原始图片
            img = Image.open(image_path)
            width, height = img.size
            
            # 计算切割的位置
            width_cut = width // 2
            height_cut_1 = height // 4
            height_cut_2 = height // 2
            height_cut_3 = (3 * height) // 4
            
            targetDir = self.GetOutDirByType('Texture2D')
            # 切割并保存子图片
            for j in range(4):  # 纵向切割
                for i in range(2):  # 横向切割
                    box = (
                        i * width_cut,
                        j * height_cut_1,
                        (i + 1) * width_cut,
                        (j + 1) * height_cut_1
                    )
                    
                    cropped_img = img.crop(box)
                    save_path = os.path.join(targetDir, f"{output_prefix}{i + 2 * j}.png")
                    cropped_img.save(save_path)
                    # cropped_img.save(f"{output_prefix}{i + 2 * j}.png")
                    print(f"Saved image: {output_prefix}{i + 2 * j}.png")
        
        except FileNotFoundError:
            print(f"File '{image_path}' not found.")
        
        except Exception as e:
            print(f"An error occurred: {e}")


    def SaveTexture2D(self, data):
        targetDir = self.GetOutDirByType('Texture2D')
        isExist = os.path.exists(targetDir)
        
        if not isExist:
            os.makedirs(targetDir)

        if data.m_Width != 0:
            outPath = os.path.join(targetDir, data.m_Name + ".png")
            try:
                print("SaveTexture2D:", outPath)
                data.image.save(outPath)

                targetDir_k = self.GetOutDirByType('Texture2D-k')
                isExist_k = os.path.exists(targetDir_k)
                if not isExist_k:
                    os.makedirs(targetDir_k)

                # fp = os.path.join(outPath, f"{data.m_Name}.png")
                # pil_img = Image.open(outPath)
                # data.image = pil_img
                # data.save()
                duo_img = ['BV_HaveFun_GnomergonOmen_Epic', 'BV_VacationHolmes_Epic', 'BV_SurferKaelthas_Epic', 'BV_OrgrimmarFaelin_Epic', 'RapunzelXyrella_Epic_512', 'HatterPutricide_Epic_512', 'BenevolentFaelin_Epic_512', 'JailbreakRafaam(Epic)_animation_512', 'JusticeJaina(Epic)_animation_512', 'BulletstormAlAkir(Epic)_animation_512', 'DeadHandPatches(Epic)_animation_512', 'DartHuntressSylvanas(Epic)_animation_512', 'StandoffJandice(Epic)_animation_512', 'OilBaronPutricide(Epic)_animation_512', 'LoneRangerReno(Epic)_animation_512', 'HE_YShaarjCookie_sketchanimation_512', 'HE_Rexxar Garrosh_sketchanimation_512', 'HE_PirateIllidan_sketchanimation_512']
                if data.m_Name in duo_img:
                    output_path = os.path.join(targetDir_k, data.m_Name + ".gif")
                    self.split_and_create_gif(outPath, output_path, data.m_Name)
                # if (data.m_Name == 'BV_HaveFun_GnomergonOmen_Epic'):
                #     output_path = os.path.join(targetDir_k, data.m_Name + ".gif")
                #     self.split_and_create_gif(outPath, output_path)
                    # self.split_image_to_gif(outPath, output_path, 500)
                elif (data.m_Name == 'Default_Emotes'):
                    self.split_Default_Emotes_image(outPath, 'Default_Emotes_')
                else:
                    output_path = os.path.join(targetDir_k, data.m_Name + ".png")
                    self.resize_and_center_crop(outPath, output_path)

            except Exception as e:
                print(traceback.format_exc())
                pass
        else:
            print(data.m_Name, "Can't be processed")

    def SaveMono(self, mono):
        # targetDir = self.GetOutDirByType('MonoBehaviour')
        # isExist = os.path.exists(targetDir)

        # if not isExist:
        #     os.makedirs(targetDir)


        print(mono, '<---Mono')
        exit()
        # outPath = os.path.join(targetDir, mono.name + ".txt")
        # if mono.script:
        #     with open(outPath, "wt", encoding="utf8") as f:
        #         try:
        #             print(type(mono.script))
        #             f.write(json.dump(mono.script.read().to_dict(), f, ensure_ascii = False, indent=4))
        #         except Exception as e:
        #             print(traceback.format_exc())
        #             pass
    def SaveMonoScript(self, data):
        # targetDir = self.GetOutDirByType('MonoScript')
        # isExist = os.path.exists(targetDir)

        # if not isExist:
        #     os.makedirs(targetDir)

        print(data, '<---MonoScript')
        # exit()
    def SaveAssetBundle(self, data):
        # targetDir = self.GetOutDirByType('MonoScript')
        # isExist = os.path.exists(targetDir)

        # if not isExist:
        #     os.makedirs(targetDir)

        print(data, '<---AssetBundle')
        # exit()
    def SaveCard(self, data):
        # targetDir = self.GetOutDirByType('MonoScript')
        # isExist = os.path.exists(targetDir)

        # if not isExist:
        #     os.makedirs(targetDir)

        print(data, '<---card')
        # exit()
    def getAnimator(self, data):
        # targetDir = self.GetOutDirByType('Animator')
        # isExist = os.path.exists(targetDir)

        # if not isExist:
        #     os.makedirs(targetDir)
        print(data, '<---')

    def getAnimationClip(self, data):
        # targetDir = self.GetOutDirByType('AnimationClip')
        # isExist = os.path.exists(targetDir)

        # if not isExist:
        #     os.makedirs(targetDir)
        print(data, '<--data-')
        print(data.m_ParsedForm.m_Name, '<--.m_ParsedForm.m_Name-')
        # showName = video_clip.m_ParsedForm.m_Name
        # showName = showName.replace(' ', '_')
        # showName = showName.replace('/', '_')
        # print(video_clip.m_ParsedForm.m_Name, showName)
        # outPath = os.path.join(targetDir, showName + ".txt")

        # with open(outPath, "wt", encoding="utf8") as f:
        #     f.write(video_clip.export())

    def UnPack(self, *args):
        self.env = UnityPy.load(self.inFile)
        all = True if len(args) == 0 else False
        
        for obj in self.env.objects:
            # print(type(obj.type), '--type--')
            print(obj.type.name, '--name--')
            # print(obj.type == "Texture2D", '--1--')
            # print(obj.type.name == "ClassIDType.Texture2D", '--2--')
            if all or (obj.type in args):
                if obj.type.name == "Texture2D":
                    data = obj.read()
                    self.SaveTexture2D(data)
                elif obj.type.name == "MonoBehaviour":
                    # mono = obj.read()
                    # self.SaveMono(mono)
                    targetDir = self.GetOutDirByType('MonoBehaviour')
                    isExist = os.path.exists(targetDir)

                    if not isExist:
                        os.makedirs(targetDir)
                    if obj.serialized_type.nodes:
                        # save decoded data
                        tree = obj.read_typetree()
                        fp = os.path.join(targetDir, f"{tree['m_Name']}.json")
                        with open(fp, "wt", encoding = "utf8") as f:
                            json.dump(tree, f, ensure_ascii = False, indent = 4)
                    else:
                        # save raw relevant data (without Unity MonoBehaviour header)
                        data = obj.read()
                        fp = os.path.join(targetDir, f"{data.name}.bin")
                        with open(fp, "wb") as f:
                            f.write(data.raw_data)
                # elif obj.type.name == "MonoScript":
                #     mono = obj.read()
                #     self.SaveMonoScript(mono)
                # elif obj.type.name == "AssetBundle":
                #     mono = obj.read()
                #     self.SaveAssetBundle(mono)
                # elif obj.type.name == "Card":
                #     mono = obj.read()
                #     self.SaveCard(mono)
                # elif obj.type.name == "AnimatorController":
                #     data = obj.read()
                #     self.getAnimator(data)
                elif obj.type.name == "AnimationClip":
                    # data = obj.read()
                    # self.getAnimationClip(data)
                    targetDir = self.GetOutDirByType('AnimationClip')
                    isExist = os.path.exists(targetDir)

                    if not isExist:
                        os.makedirs(targetDir)
                    if obj.serialized_type.nodes:
                        # save decoded data
                        tree = obj.read_typetree()
                        fp = os.path.join(targetDir, f"{tree['m_Name']}.json")
                        with open(fp, "wt", encoding = "utf8") as f:
                            json.dump(tree, f, ensure_ascii = False, indent = 4)
                    else:
                        # save raw relevant data (without Unity AnimationClip header)
                        data = obj.read()
                        fp = os.path.join(targetDir, f"{data.name}.bin")
                        with open(fp, "wb") as f:
                            f.write(data.raw_data)
                elif obj.type.name == "AssetBundle":
                    # data = obj.read()
                    # self.getAssetBundle(data)
                    targetDir = self.GetOutDirByType('AssetBundle')
                    isExist = os.path.exists(targetDir)

                    if not isExist:
                        os.makedirs(targetDir)
                    if obj.serialized_type.nodes:
                        # save decoded data
                        tree = obj.read_typetree()
                        fp = os.path.join(targetDir, f"{tree['m_Name']}.json")
                        with open(fp, "wt", encoding = "utf8") as f:
                            json.dump(tree, f, ensure_ascii = False, indent = 4)
                    else:
                        # save raw relevant data (without Unity AssetBundle header)
                        data = obj.read()
                        fp = os.path.join(targetDir, f"{data.name}.bin")
                        with open(fp, "wb") as f:
                            f.write(data.raw_data)
                elif obj.type.name == "SortingGroup":
                    continue
                elif obj.type.name == "Transform":
                    continue
                elif obj.type.name == "MeshRenderer":
                    continue
                elif obj.type.name == "MeshFilter":
                    continue
                elif obj.type.name == "ParticleSystem":
                    continue
                elif obj.type.name == "Animation":
                    continue
                elif obj.type.name == "ParticleSystemRenderer":
                    continue
                else:
                    print(obj.type.name, '--not support--')
                    # targetDir = self.GetOutDirByType(obj.type.name)
                    # isExist = os.path.exists(targetDir)

                    # if not isExist:
                    #     os.makedirs(targetDir)
                    # if obj.serialized_type.nodes:
                    #     # save decoded data
                    #     tree = obj.read_typetree()
                    #     fp = os.path.join(targetDir, f"{tree['m_Name']}.json")
                    #     with open(fp, "wt", encoding = "utf8") as f:
                    #         json.dump(tree, f, ensure_ascii = False, indent = 4)
                    # else:
                    #     # save raw relevant data (without Unity AssetBundle header)
                    #     data = obj.read()
                    #     fp = os.path.join(targetDir, f"{data.name}.bin")
                    #     with open(fp, "wb") as f:
                    #         f.write(data.raw_data)



def Usage(argv):
    UsageMessage = os.path.basename(__file__) + ' -i <input> -o <outputpath>'

    inp = ''
    outDir = ''
    filterConfig = None

    try:
        opts, args = getopt.getopt(argv, "hi:o:f:")
    except getopt.GetoptError:
        print(UsageMessage)
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print(UsageMessage)
            sys.exit()
        elif opt in ("-i"):
            inp = arg
        elif opt in ("-o"):
            outDir = arg
        elif opt in ("-f"):
            filterConfig = arg

    if '' == inp or '' == outDir:
        print(UsageMessage)
        sys.exit(2)

    unpacker = UnpackAutoEmote(inp, outDir)
    if filterConfig == None:
        unpacker.UnPack()
    else:
        unpacker.UnPack(filterConfig)


# 读取Unity打包文件的GUID
def read_unity_packed_file_guid(file_path):
    # 打开文件
    with open(file_path, 'rb') as file:
        # 读取前16个字节，即GUID的长度
        file.seek(4)
        guid_length_bytes = file.read(16)
        
        # 解析GUID的长度
        guid_length = struct.unpack('<L', guid_length_bytes[:4])[0]
        
        # 读取GUID
        file.seek(20)
        guid_bytes = file.read(guid_length)
        
        # 将GUID转换为字符串
        guid = ''.join('%02X' % b for b in guid_bytes)
        return guid
    
if __name__ == "__main__":
    Usage(sys.argv[1:])

