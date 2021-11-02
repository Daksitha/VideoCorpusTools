import json
import logging
import time




if __name__ == '__main__':
    import argparse
    import datetime

    logging.basicConfig(filename='log_merge_json{}.log'.format(datetime.datetime.now().strftime('%M_%S_%d_%m_%Y')),
                        level=logging.DEBUG)
    logging.info("=============== Start at {} ==================".format(datetime.datetime.now()))

    parser = argparse.ArgumentParser(description='Interactively edit a rectangular area in a video. '
                                                 'Useful to manually set cropping bounds.')
    parser.add_argument('--jOne_path',
                        help='Path to the json first json',
                        required=True)
    parser.add_argument('--jOne_name',
                        help='name of the json. This will be used in the json merge',
                        required=True)
    parser.add_argument('--jTwo_path',
                        help='Path to the json first json',
                        required=True)
    parser.add_argument('--jTwo_name',
                        help='name of the json. This will be used in the json merge',
                        required=True)
    parser.add_argument('--out_path',
                        help='path to save the merged json',
                        required=True)

    args = parser.parse_args()

    merged_json = {}

    with open(args.jOne_path, "r") as jOne:
        with open (args.jTwo_path , "r") as jTwo:
            jOne_bounds_dict = json.load(jOne)
            jTwo_bounds_dict = json.load(jTwo)
            # NOTE: inbound json format {"name.m4v": [{"crop_area": {"x":0, "y": 0, "width": 377, "height": 570},
            # "metadata": { "nb_frames": "110431", "is_crop_selected": true, "v_width": 718, "v_height": 576}}], ...}
            # video_name = os.path.basename(args.invideo)
            num_videos_indx = 0
            for video_name in jOne_bounds_dict:
                num_videos_indx += 1

                if video_name in jTwo_bounds_dict:
                    merged_json[video_name] = {
                        '{}'.format(args.jOne_name): jOne_bounds_dict[video_name],
                        '{}'.format(args.jTwo_name): jTwo_bounds_dict[video_name]

                    }

    # dump json
    output_fname = args.jTwo_name+"_"+ args.jTwo_name  + "_" + time.strftime("%Y%m%d-%H%M") + ".json"
    out_directory = args.out_path + "/" + output_fname
    with open(out_directory, 'w') as f:
        json.dump(merged_json, f)
        print("{0} created at {1}.json".format(output_fname, out_directory))
        logging.info("{0} created at {1}.json".format(output_fname, out_directory))




    logging.info("=============== End at {} ==================".format(datetime.datetime.now()))
