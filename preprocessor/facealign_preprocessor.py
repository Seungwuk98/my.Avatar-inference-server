from preprocessor.abc_preprocessor import preprocessor
import face_alignment
from my_avatar_ai.ffhq_align import image_align_68
import os

class facealign_preprocessor(preprocessor):
    def __init__(self) -> None:
        self.landmarks_detector = face_alignment.FaceAlignment(
            face_alignment.LandmarksType._3D, flip_input=False
        )

    
    def preprocess(self, input_path) -> str:
        # 얼굴 이미지 조정(face-alignment) 전처리 수행
        try:
            face_landmarks = self.landmarks_detector.get_landmarks(input_path)
        except:
            print(f"Cannot detect face of {input_path}")
            return None

        img_name, extension = os.path.splitext(input_path)
        aligned_path = img_name + "-align" + extension
        image_align_68(input_path, aligned_path, face_landmarks[0])
        return aligned_path