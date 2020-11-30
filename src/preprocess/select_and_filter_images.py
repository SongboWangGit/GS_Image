import os
import shutil
import pandas as pd
from matplotlib import pyplot as plt
from xml.dom.minidom import parse

from lxml import etree


def select_images(selected_list, original_folders, out_folders):

    with open(selected_list, 'r') as fin:
        for line in fin.readlines():
            gs_id = line.strip()

            gs_path = os.path.join(original_folders, gs_id)
            if not os.path.exists(gs_path):
                print("Not exists ", gs_id)

            else:
                out_path = os.path.join(out_folders, gs_id)
                shutil.copytree(gs_path, out_path)
                # cmd_str = 'cp -r {0} {1}'.format(gs_path, out_path)
                # os.system(cmd_str)


def filter_gcid_no_images(in_dir):

    all_gs_ids = os.listdir(in_dir)

    for gs_id in all_gs_ids:
        id_path = os.path.join(in_dir, gs_id)
        id_gs_path = os.path.join(id_path, 'IMAGE50HTTP')

        # filter none data
        if not os.path.exists(id_gs_path):
            shutil.rmtree(id_path)
            print(id_gs_path)
        else:
            sub_folders = os.listdir(id_gs_path)
            if len(sub_folders) == 0:
                shutil.rmtree(id_path)
                print(id_gs_path)


def tag_no_image_item(list_file, changed_file):
    file = pd.read_excel(changed_file, dtype=str)

    none_list = []
    with open(list_file, 'r') as fin:
        for line in fin.readlines():
            gc_id = line.strip()
            none_list.append(gc_id)

    file['备注'] = ''

    for index, row in file.iterrows():
        if row['影像号'] in none_list:
            row['备注'] = '影像缺失'
    file.to_excel('data3.xlsx', index=False, na_rep='1')

def stats_images_size(in_dir):
    all_gs_ids = os.listdir(in_dir)

    all_sizes = []
    size_stats = {}
    for gs_id in all_gs_ids:
        id_path = os.path.join(in_dir, gs_id)
        id_gs_path = os.path.join(id_path, 'IMAGE50HTTP')
        sub_folders = os.listdir(id_gs_path)

        if 'AccuImage.dir' in sub_folders:
            sub_folders.remove('AccuImage.dir')
        if len(sub_folders) != 1:
            print(sub_folders)

        id_image_path = os.path.join(id_gs_path, sub_folders[0])
        if not os.path.exists(id_image_path):
            print(gs_id)

        images = os.listdir(id_image_path)
        if 'AccuImage.dir' in images:
            images.remove('AccuImage.dir')
        for tmp in images:
            size = int(os.path.getsize(os.path.join(id_image_path, tmp)) / float(1024))

            if size > 1500:
                # print(gs_id, size)
                continue
            all_sizes.append(size)
            if size not in size_stats.keys():
                size_stats[size] = 1
            else:
                size_stats[size] += 1
    sorted_size_starts = sorted(size_stats.items(), key=lambda item: item[0])
    print(sorted_size_starts)

    bins_interval = 10
    margin = 1
    bins = range(min(all_sizes), max(all_sizes) + bins_interval - 1, bins_interval)

    plt.xlim(min(all_sizes) - margin, max(all_sizes) + margin)
    plt.xlabel('img size')
    plt.ylabel('cumulative number')
    plt.hist(x=all_sizes, bins=bins, histtype='step', cumulative=True)
    plt.show()

def extract_patient_from_xml(data_path, excel_path):

    file = pd.read_excel(excel_path, dtype=str)

    file['姓名'] = ''
    file['性别'] = ''
    file['出生日期'] = ''

    for index, row in file.iterrows():
        id = row['影像号']
        id_path = os.path.join(data_path, id)
        xml_file = os.path.join(id_path, "Index.XML")
        # print(id)
        if not os.path.exists(xml_file):
            print(os.listdir(id_path))

        # parse xml file
        try:
            tree = etree.parse(xml_file)
        except:
            print(id)
        else:
            tree_root = tree.getroot()
            tree_patient = tree_root.find('PATIENT').find('row')
            patient_name = tree_patient.get("PATIENTNAME")
            patient_sex = tree_patient.get("SEX")
            patient_birday = tree_patient.get("BIRTHDAY")

            row['姓名'] = patient_name
            row['性别'] = patient_sex
            row['出生日期'] = patient_birday
    file.to_excel('data3.xlsx', index=False, na_rep='1')

    # tree = etree.parse("D:/Data/Gastric/origin_data/selected/20130905000140/Index.XML")
    # tree_root = tree.getroot()
    # tree_patient = tree_root.find('PATIENT').find('row')
    # print(tree_patient.get("PATIENTNAME"))




    # with open(list_file) as fin:
    #     for line in fin.readlines():
    #         id = line.strip()
    #         id_path = os.path.join(data_path, id)
    #         xml_file = os.path.join(id_path, "Index.XML")
    #
    #         if not os.path.exists(xml_file):
    #             print(os.listdir(id_path))

if __name__ == '__main__':
    # select_images('D:/Data/Gastric/origin_data/gs_ulcer_list.txt', 'E:/Copy/Data/Gastric/胃镜原始数据/1', 'D:/Data/Gastric/origin_data/selected')
    # filter_gcid_no_images('D:/Data/Gastric/origin_data/selected')
    # tag_no_image_item('D:/Data/Gastric/origin_data/none_list.txt', 'D:/Data/Gastric/origin_data/胃肠镜 - 溃疡 - 胃镜.xlsx')
    # stats_images_size('D:/Data/Gastric/origin_data/selected')
    #
    extract_patient_from_xml("D:/Data/Gastric/origin_data/selected", 'D:/Data/Gastric/origin_data/胃肠镜 - 溃疡 - 胃镜 - 含缺失.xlsx')


