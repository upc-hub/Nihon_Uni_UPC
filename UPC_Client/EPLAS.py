import cv2
import json
import numpy as np
import argparse
import os
import time
import shutil
import codecs
import math

# Each name in this body_name list according to body name of openpose index.
body_name = ["xx", "xx", "xx", "right elbow", "right hand", "xx", "left elbow", "left hand", "xx", "xx", "right knee",
             "right foot", "xx", "left knee", "left foot", "xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx"]


class ElaspSystem:


    def __init__(self, filepath):
        print ("Hein Htet")
        self.filepath = filepath

    def get_all_keypoint(self, user_keypoint_file, real_keypoint_file):
        """

        :param user_keypoint_file: user keypoint file
        :param real_keypoint_file: instructor keypoint file
        :return:User and right keypoint corridor.
        """
        x_coordinate, x_real_coordinate, y_coordinate, y_real_coordinate = [], [], [], []
        with codecs.open(user_keypoint_file, 'r+') as user_keypoint:
            user = json.load(user_keypoint)
            for i in range(0, len(user['people'][0]['pose_keypoints_2d']), 3):
                if i != len(user['people'][0]['pose_keypoints_2d']):
                    x_coordinate.append(user['people'][0]['pose_keypoints_2d'][i])  # x coordinate of user
                    y_coordinate.append(user['people'][0]['pose_keypoints_2d'][i + 1])  # y coordinate of instructor
                else:
                    break
        with codecs.open(real_keypoint_file, 'r+') as real_keypoint:
            instructor = json.load(real_keypoint)
            for j in range(0, len(instructor['people'][0]['pose_keypoints_2d']), 3):
                if j != len(instructor['people'][0]['pose_keypoints_2d']):
                    x_real_coordinate.append(instructor['people'][0]['pose_keypoints_2d'][j])  # x' coordinate of user
                    y_real_coordinate.append(
                        instructor['people'][0]['pose_keypoints_2d'][j + 1])  # y' coordinate of instructor
                else:
                    break
        x_coordinate = np.array(x_coordinate)
        y_coordinate = np.array(y_coordinate)
        x_real_coordinate = np.array(x_real_coordinate)
        y_real_coordinate = np.array(y_real_coordinate)

        return x_coordinate, x_real_coordinate, y_coordinate, y_real_coordinate

    def get_coefficient(self, x_coordinate, x_real_coordinate, y_coordinate, y_real_coordinate):
        """

        :param x_coordinate: x coordinate of user.
        :param x_real_coordinate: x coordinate of instructor.
        :param y_coordinate:
        :param y_real_coordinate:
        :return: coefficient a and b.
        """
        X_mean = np.mean(x_coordinate)
        X_next_mean = np.mean(x_real_coordinate)
        Y_mean = np.mean(y_coordinate)
        Y_next_mean = np.mean(y_real_coordinate)

        num = 0
        den = 0
        for i in range(len(x_coordinate)):
            num += (x_coordinate[i] - X_mean) * (x_real_coordinate[i] - X_next_mean)  # calculate a,b of x' = ax + b
            den += (x_coordinate[i] - X_mean) ** 2
        a_x = num / den
        b_x = X_next_mean - a_x * X_mean

        num = 0
        den = 0

        for i in range(len(y_coordinate)):
            num += (y_coordinate[i] - Y_mean) * (y_real_coordinate[i] - Y_next_mean)  # calculate a,b of y' = ay + b
            den += (y_coordinate[i] - Y_mean) ** 2
        a_y = num / den
        b_y = Y_next_mean - a_y * Y_mean

        a_x = round(a_x, 2)
        b_x = round(b_x, 2)
        a_y = round(a_y, 2)
        b_y = round(b_y, 2)

        return a_x, b_x, a_y, b_y

    def calc_ls(self, a_x, b_x, a_y, b_y, x_coordinate, y_coordinate):  # calculate least square
        x_corridor_result, y_corridor_result = [], []

        for i in x_coordinate:
            x_corridor_result.append(round(a_x * i + b_x, 2))
        for j in y_coordinate:
            y_corridor_result.append(round(a_y * j + b_y, 2))

        return x_corridor_result, y_corridor_result

    def calc_ed(self, x_real_coordinate, y_real_coordinate, x_coordinate_result,
                y_coordinate_result):  # calculate Euclid distances
        ed_result = []

        x_coordinate_result = np.array(x_coordinate_result)
        y_coordinate_result = np.array(y_coordinate_result)

        for i in range(0, len(x_coordinate_result)):
            each_ed = np.sqrt(
                np.power((x_coordinate_result[i] - x_real_coordinate[i]), 2) + np.power(
                    (y_coordinate_result[i] - y_real_coordinate[i]),
                    2))  # Euclidean distance formula
            ed_result.append(round(each_ed, 2))

        return ed_result

    def calc_threshold(self, ED_result):  # calculate threshold
        ED_result = np.array(ED_result)
        mean_value = np.mean(ED_result)
        std_value = np.std(ED_result)
        mean_value = round(float(mean_value), 2)
        std_value = round(float(std_value), 2)
        #print('mean_value: ', mean_value)  # The average of Euclidean distance
        #print('std_value: ', std_value)  # Standard value of Euclidean distance
        threshold = round(mean_value + 2*std_value, 2)
        return threshold

    def calc_irin(self, ed, x_error, y_error, wrong_index):
        wrong_result = []
        ED = ed  # Euclid Distance
        x = x_error  # x_error
        y = y_error  # y_error
        for i in range(0, len(ed)):
            A = (1 / math.cos(x[i] / ED[i]))  # θ=cos^-1{A}
            output = float()
            if (y[i] > 0):
                output = ((math.pi) * 2 - A)
            else:
                output
            if output >= -0.39 and output < 0.39:
                keypoint = "shift {} right ".format(body_name[i])
            elif output >= 0.39 and output < 1.18:
                keypoint = "shift {} upper right ".format(body_name[i])
            elif output >= 1.18 and output < 1.96:
                keypoint = "shift {} upper ".format(body_name[i])
            elif output >= 1.96 and output < 2.75:
                keypoint = "shift {} upper left ".format(body_name[i])
            elif output >= 2.75 and output < 3.53:
                keypoint = "shift {} left ".format(body_name[i])
            elif output >= 3.53 and output < 4.32:
                keypoint = "shift {} lower left ".format(body_name[i])
            elif output >= 4.32 and output < 5.10:
                keypoint = "shift {} lower ".format(body_name[i])
            elif output >= 5.10 and output < 5.89:
                keypoint = "shift {} lower right".format(
                    body_name[i])  # keypoint information need to combine with prev. program
            if i in wrong_index:
                print('Result:', output)
                print('Correction Message:', keypoint)

    def mark_image(self, ed_result, threshold, x_corr, y_corr, filepath, filepath3, output_path, flag):
        wrong_index = []
        for i in range(0, len(ed_result)):
            if ed_result[i] - threshold > 0:
                wrong_index.append(i)
        image = cv2.imread(filepath)
        for i in wrong_index:
            cv2.rectangle(image, (int(x_corr[i]) - 10, int(y_corr[i]) - 10),
                          (int(x_corr[i]) + 10, int(y_corr[i]) + 10),
                          (0, 255, 0), 1)  # Wrong action are marked with squares
        name_time = str(time.time())
        cv2.imencode('.png', image)[1].tofile(filepath3 + name_time + '_wrong.png')
        shutil.move(filepath3 + name_time + '_wrong.png', output_path + "/" + str(flag) + "_wrong.png")
        return wrong_index

    # def mark_image_2(self, ed_result, threshold, x_corr, y_corr, filepath, filepath3, output_path, flag):
    #     wrong_index = []
    #     for i in range(0, len(ed_result)):
    #         if ed_result[i] - threshold > 0:
    #             wrong_index.append(i)
    #     image = cv2.imread(filepath)
    #     for i in wrong_index:
    #         cv2.rectangle(image, (int(x_corr[i]) - 10, int(y_corr[i]) - 10),
    #                       (int(x_corr[i]) + 10, int(y_corr[i]) + 10),
    #                       (0, 255, 0), 1)  # Wrong action are marked with squares
    #     name_time = str(time.time())
    #     cv2.imencode('.png', image)[1].tofile(filepath3 + name_time + '_wrong.png')
    #     shutil.move(filepath3 + name_time + '_wrong.png', output_path + "\\" + str(flag) + "_wrong.png")
    #     return wrong_index


if __name__ == '__main__':
    flag = 0  # for distinguish different image name
    dir_list = []
    parser = argparse.ArgumentParser('please input user keypoints json file and instructor keypoints json file')
    parser.add_argument('-f', '--filepath', help="All files folder")  # user image keypoints
    args = parser.parse_args()

    root_path = args.filepath
    #print (root_path)
    output_path = root_path + "/output/"  # input your output folder absolute filepath

    for dir_i in os.listdir(root_path):  # the same input absolute filepath as before
        if os.path.isdir(root_path + "/" + dir_i):
            dir_list.append(root_path + "/" + dir_i)
    #print (dir_list)
    for i in dir_list:
        #print(i)
        user_keypoint_path = i + "/keypoints/"
        instructor_path = i + "/instructor/"
        picture_path = i + "/picture/"
        print (user_keypoint_path)
        print (instructor_path)
        print (picture_path)
        user_keypoint_list, instructor_list, picture_list = [], [], []
        i, j, k = 0, 0, 0

        for root, dirs, files in os.walk(user_keypoint_path):  # 遍历统计
            #print (root, dirs, files)
            for x in files:
                user_keypoint_list.append(root + x)
                i += 1
        for root1, dirs1, files1 in os.walk(instructor_path):
            for y in files1:
                instructor_list.append(root1 + y)
                j += 1
        for root2, dirs2, files2 in os.walk(picture_path):
            for z in files2:
                picture_list.append(root2 + z)
                k += 1
        #print (i, j, k)
        es = ElaspSystem(root_path)
        #print (es)
        for each_user_keypoint, each_instructor, each_picture in zip(user_keypoint_list, instructor_list, picture_list):
            x_corridor, x_real_corridor, y_corridor, y_real_corridor = es.get_all_keypoint(each_user_keypoint,
                                                                                           each_instructor)
            print('x coordinate of user: ', x_corridor)
            print('x\' coordinate of user: ', x_real_corridor)
            print('y coordinate of user: ', y_corridor)
            print('y\' coordinate of user: ', y_real_corridor)
            a_x, b_x, a_y, b_y = es.get_coefficient(x_corridor, x_real_corridor, y_corridor, y_real_corridor)
            print('a of x coordinate: ', a_x, 'b of x coordinate: ', b_x, 'a of y coordinate: ', a_y,
                  'b of y coordinate: ',
                  b_y)
            x_corr_result, y_corr_result = es.calc_ls(a_x, b_x, a_y, b_y, x_corridor, y_corridor)
            #print('x_conv: ', x_corr_result)
            #print('y_conv: ', y_corr_result)
            ed_result = es.calc_ed(x_real_corridor, y_real_corridor, x_corr_result, y_corr_result)

            #print('Euclid distance: ', ed_result)
            threshold = es.calc_threshold(ed_result)
            #print('threshold: ', threshold)
            wrong_index = es.mark_image(ed_result, threshold, x_corridor, y_corridor, each_picture, picture_path,
                                        output_path, flag)
            es.calc_irin(ed_result, x_real_corridor - x_corr_result, y_real_corridor - y_corr_result, wrong_index)
            flag += 1
