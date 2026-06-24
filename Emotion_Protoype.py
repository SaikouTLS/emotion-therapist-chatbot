import cv2
from deepface import DeepFace

# Start the webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame from the webcam
    ret, frame = cap.read()

    # Analyze the emotions using DeepFace
    try:
        # DeepFace analyzes the frame and returns a list of analysis results if multiple faces are detected
        analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        
        # Check if analysis is a list (multiple faces detected) and access the first result
        if isinstance(analysis, list):
            analysis = analysis[0]
        
        # Extract the emotion probabilities (confidence values)
        emotion_confidences = analysis['emotion']
        
        # Display each emotion and its confidence percentage on the video feed
        y_offset = 50  # Start displaying from this position
        for emotion, confidence in emotion_confidences.items():
            text = f"{emotion}: {confidence:.2f}%"
            cv2.putText(frame, text, (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
            y_offset += 30  # Move the next text down
        
        # Optionally, show the dominant emotion at the top
        dominant_emotion = analysis['dominant_emotion']
        cv2.putText(frame, f"Dominant emotion: {dominant_emotion}", (50, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    
    except Exception as e:
        # If no face is detected or any other error occurs, show error message
        print("Error:", e)
        cv2.putText(frame, "No face detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # Display the resulting frame with emotion probabilities
    cv2.imshow('Emotion Detection', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
