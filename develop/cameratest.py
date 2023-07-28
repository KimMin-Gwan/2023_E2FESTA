import pyrealsense2 as rs

def main():
    # 카메라 초기화
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)  # 해상도와 프레임 속도 설정

    # 스트리밍 시작
    pipeline.start(config)

    try:
        while True:
            # 프레임 얻기
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()

            # 프레임이 유효한지 확인
            if not depth_frame:
                continue

            # 프레임 데이터 얻기
            distance = depth_frame.get_distance(640, 360)  # 중앙점의 거리를 얻음 (x, y)

            # 출력
            print(f"거리: {distance:.2f} 미터")

    finally:
        # 종료 시 리소스 해제
        pipeline.stop()

if __name__ == "__main__":
    main()