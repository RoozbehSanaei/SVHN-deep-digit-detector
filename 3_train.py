#-*- coding: utf-8 -*-

import object_detector.file_io as file_io
import object_detector.factory as factory
import argparse as ap

DEFAULT_HNM_OPTION = True
DEFAULT_CONFIG_FILE = "conf/car_side.json"
DEFAULT_PATCH_SIZE = (32, 96)

if __name__ == "__main__":
    
    parser = ap.ArgumentParser()
    parser.add_argument('-c', "--config", help="Configuration File", default=DEFAULT_CONFIG_FILE)
    parser.add_argument('-ph', "--patch_h_size", help="Patch Size of Height", default=DEFAULT_PATCH_SIZE[0], type=int)
    parser.add_argument('-pw', "--patch_w_size", help="Patch Size of Width", default=DEFAULT_PATCH_SIZE[1], type=int)
    parser.add_argument('-i', "--include_hnm", help="Include Hard Negative Mined Set", default=DEFAULT_HNM_OPTION, type=bool)
    args = vars(parser.parse_args())
    
    conf = file_io.FileJson().read(args["config"])
    patch_size = (args["patch_h_size"], args["patch_w_size"])
    
    #1. Load Features and Labels
    getter = factory.Factory.create_extractor(conf["descriptor"]["algorithm"], 
                                              conf["descriptor"]["parameters"], 
                                              patch_size, 
                                              conf["extractor"]["output_file"])
    # getter.summary()
    data = getter.get_dataset(include_hard_negative=args["include_hnm"])
    
    y = data[:, 0]
    X = data[:, 1:]
 
    #2. Load classifier and Train
    cls = factory.Factory.create_classifier(conf["classifier"]["algorithm"], 
                                            conf["classifier"]["parameters"])
    
    cls.train(X, y)
    print "[INFO] Training result is as follows"
    print cls.evaluate(X, y)
 
    #3. Save classifier
    cls.dump(conf["classifier"]["output_file"])


