import argparse
from src.video_processing import processar_video

def main():
    parser = argparse.ArgumentParser(description="Processar vídeo com ou sem GPU.")
    
    parser.add_argument('video_path', type=str, help="Caminho para o arquivo de vídeo")
    
    # Flag opcional para usar GPU
    parser.add_argument('--gpu', action='store_true', help="Use GPU para processamento")

    args = parser.parse_args()
    
    processar_video(args.video_path, gpu=args.gpu)

if __name__ == "__main__":
    main()
