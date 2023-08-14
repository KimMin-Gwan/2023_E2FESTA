"""
* Project : 2023CDP OCR(Optical Character Recognition)
* Program Purpose and Features :
* - Recognize text
* Author : SJ Yang
* First Write Date : 2023.08.09
* ==========================================================================
* Program history
* ==========================================================================
* Author    		Date		    Version		History
* SJ Yang			2023.08.09      v0.10	    first write
* SJ Yang           2023.08.09      v1.00       variable fix
"""


from OCR_model.dataset_fix import *
from OCR_model.model_fix import *
from OCR_model.utils_fix import *

from TextRecognition.constant import *

import string
import argparse  # argument(명령어)를 읽고 parsing(파씽)해주는 라이브러리

import torch
import torch.backends.cudnn as cudnn
import torch.utils.data
import torch.nn.functional as F


'''from utils_fix import AttnLabelConverter 
from dataset_fix import RawDataset, AlignCollate
from model_fix import Model'''

from TextRecognition.constant import *

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class Dectector():
    def demo(self, camera):
        """ model configuration """
        if 'Attn' in PREDICTION:
            converter = AttnLabelConverter(CHARACTER)
        num_class = len(converter.character)

        if RGB:
            INPUT_CHANNEL = 3
        model = Model(num_class)
        print('model input parameters', IMG_HEIGHT, IMG_WIDTH, NUM_FIDUCIAL, INPUT_CHANNEL, OUTPUT_CHANNEL,
            HIDDEN_SIZE, num_class, BATCH_MAX_LENGTH, TRANSFORMATION, FEATURE_EXTRACTION,
            SEQUENCE_MODELING, PREDICTION)
        model = torch.nn.DataParallel(model).to(device)

        # load model
        print('loading pretrained model from %s' % SAVED_MODEL)
        #model.load_state_dict(torch.load(opt.saved_model, map_location=device))
        model.load_state_dict(torch.load(SAVED_MODEL, map_location=device))

        # prepare data. two demo images from https://github.com/bgshih/crnn#run-demo
        AlignCollate_demo = AlignCollate(imgH=IMG_HEIGHT, imgW=IMG_WIDTH, keep_ratio_with_pad=False)
        demo_data = RawDataset(root=frame)  # use RawDataset
        
        #demo_data =
        
        demo_loader = torch.utils.data.DataLoader(
            demo_data, batch_size=BATCH_SIZE,
            shuffle=False,
            num_workers=int(WORKERS),
            collate_fn=AlignCollate_demo, pin_memory=True)

        # predict
        model.eval()
        with torch.no_grad():
            for image_tensors, image_path_list in demo_loader:
                batch_size = image_tensors.size(0)
                image = image_tensors.to(device)
                # For max length prediction
                length_for_pred = torch.IntTensor([BATCH_MAX_LENGTH] * batch_size).to(device)
                text_for_pred = torch.LongTensor(batch_size, BATCH_MAX_LENGTH + 1).fill_(0).to(device)

                if 'CTC' in PREDICTION:
                    preds = model(image, text_for_pred)

                    # Select max probabilty (greedy decoding) then decode index to character
                    preds_size = torch.IntTensor([preds.size(1)] * batch_size)
                    _, preds_index = preds.max(2)
                    # preds_index = preds_index.view(-1)
                    preds_str = converter.decode(preds_index, preds_size)

                else:
                    preds = model(image, text_for_pred, is_train=False)

                    # select max probabilty (greedy decoding) then decode index to character
                    _, preds_index = preds.max(2)
                    preds_str = converter.decode(preds_index, length_for_pred)


                log = open(f'./log_demo_result.txt', 'a')
                dashed_line = '-' * 80
                head = f'{"image_path":25s}\t{"predicted_labels":25s}\tconfidence score'
                
                print(f'{dashed_line}\n{head}\n{dashed_line}')
                log.write(f'{dashed_line}\n{head}\n{dashed_line}\n')

                preds_prob = F.softmax(preds, dim=2)
                preds_max_prob, _ = preds_prob.max(dim=2)
                for img_name, pred, pred_max_prob in zip(image_path_list, preds_str, preds_max_prob):
                    if 'Attn' in PREDICTION:
                        pred_EOS = pred.find('[s]')
                        pred = pred[:pred_EOS]  # prune after "end of sentence" token ([s])
                        pred_max_prob = pred_max_prob[:pred_EOS]

                    # calculate confidence score (= multiply of pred_max_prob)
                    confidence_score = pred_max_prob.cumprod(dim=0)[-1]

                    print(f'{img_name:25s}\t{pred:25s}\t{confidence_score:0.4f}')
                    log.write(f'{img_name:25s}\t{pred:25s}\t{confidence_score:0.4f}\n')

                log.close()
                
    def run_module(self):
        parser = argparse.ArgumentParser()  #파서 생성
        #파서가 구분할 명령어 추가
        """ Data processing """
        # 추가 옵션을 받는 경우 action = 'store
        # 추가 옵션을 받지 않고, 옵션의 유/무만 필요한 경우 action = 'store_true'
        #parser.add_argument('--rgb', action='store_true', help='use rgb input')
        
        #parser.add_argument('--PAD', action='store_true', help='whether to keep ratio then pad for image resize')
        #config 객체 생성
        #opt = parser.parse_args() #파서의 구문을 가지고 있는 객체

        """ vocab / character number configuration """

        cudnn.benchmark = True
        cudnn.deterministic = True
        #num_gpu = torch.cuda.device_count()

        self.demo()
        
if __name__ == '__main__':
    predict = Dectector()
    predict.run_module()