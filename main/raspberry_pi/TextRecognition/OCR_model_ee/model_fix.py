"""
Copyright (c) 2019-present NAVER Corp.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import torch.nn as nn
import sys, os

from OCR_model.transformation import TPS_SpatialTransformerNetwork
from OCR_model.feature_extraction_fix import ResNet_FeatureExtractor
from OCR_model.sequence_modeling import BidirectionalLSTM
from OCR_model.prediction import Attention

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from constant import *

class Model(nn.Module):

    def __init__(self, num_class):
        super(Model, self).__init__()
        #self.opt = opt
        self.stages = {'Trans': TRANSFORMATION, 'Feat': FEATURE_EXTRACTION,
                       'Seq': SEQUENCE_MODELING, 'Pred': PREDICTION}

        """ Transformation """
        if TRANSFORMATION == 'TPS':
            self.Transformation = TPS_SpatialTransformerNetwork(
                F=NUM_FIDUCIAL, I_size=(IMG_HEIGHT, IMG_WIDTH), I_r_size=(IMG_HEIGHT, IMG_WIDTH), I_channel_num=INPUT_CHANNEL)
        else:
            print('No Transformation module specified')

        """ FeatureExtraction """
        if FEATURE_EXTRACTION == 'ResNet':
            self.FeatureExtraction = ResNet_FeatureExtractor(INPUT_CHANNEL, OUTPUT_CHANNEL)
        else:
            raise Exception('No FeatureExtraction module specified')
        self.FeatureExtraction_output = OUTPUT_CHANNEL  # int(imgH/16-1) * 512
        self.AdaptiveAvgPool = nn.AdaptiveAvgPool2d((None, 1))  # Transform final (imgH/16-1) -> 1

        """ Sequence modeling"""
        if SEQUENCE_MODELING == 'BiLSTM':
            self.SequenceModeling = nn.Sequential(
                BidirectionalLSTM(self.FeatureExtraction_output, HIDDEN_SIZE, HIDDEN_SIZE),
                BidirectionalLSTM(HIDDEN_SIZE, HIDDEN_SIZE, HIDDEN_SIZE))
            self.SequenceModeling_output = HIDDEN_SIZE
        else:
            print('No SequenceModeling module specified')
            self.SequenceModeling_output = self.FeatureExtraction_output

        """ Prediction """
        if PREDICTION == 'CTC':
            self.Prediction = nn.Linear(self.SequenceModeling_output, num_class)
        elif PREDICTION == 'Attn':
            self.Prediction = Attention(self.SequenceModeling_output, HIDDEN_SIZE, num_class)
        else:
            raise Exception('Prediction is neither CTC or Attn')

    def forward(self, input, text, is_train=True):
        """ Transformation stage """
        if not self.stages['Trans'] == "None":
            input = self.Transformation(input)

        """ Feature extraction stage """
        visual_feature = self.FeatureExtraction(input)
        visual_feature = self.AdaptiveAvgPool(visual_feature.permute(0, 3, 1, 2))  # [b, c, h, w] -> [b, w, c, h]
        visual_feature = visual_feature.squeeze(3)

        """ Sequence modeling stage """
        if self.stages['Seq'] == 'BiLSTM':
            contextual_feature = self.SequenceModeling(visual_feature)
        else:
            contextual_feature = visual_feature  # for convenience. this is NOT contextually modeled by BiLSTM

        """ Prediction stage """
        if self.stages['Pred'] == 'CTC':
            prediction = self.Prediction(contextual_feature.contiguous())
        else:
            prediction = self.Prediction(contextual_feature.contiguous(), text, is_train, batch_max_length=BATCH_MAX_LENGTH)

        return prediction
