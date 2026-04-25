from backend.services.aegis_service import analyze_video

data = analyze_video("data/videos/test_near_miss.mp4")


print(data[:2])