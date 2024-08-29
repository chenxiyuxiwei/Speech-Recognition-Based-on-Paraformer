import requests
from io import BytesIO
import speech_recognition as sr
import pandas as pd
from funasr import AutoModel


def calculate_wer(reference: str, hypothesis: str) -> float:
    reference_words = reference.split()
    hypothesis_words = hypothesis.split()
    N = len(reference_words)
    dp = [[0] * (len(hypothesis_words) + 1) for _ in range(len(reference_words) + 1)]
    for i in range(len(reference_words) + 1):
        dp[i][0] = i
    for j in range(len(hypothesis_words) + 1):
        dp[0][j] = j
    for i in range(1, len(reference_words) + 1):
        for j in range(1, len(hypothesis_words) + 1):
            if reference_words[i - 1] == hypothesis_words[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                substitution = dp[i - 1][j - 1] + 1
                insertion = dp[i][j - 1] + 1
                deletion = dp[i - 1][j] + 1
                dp[i][j] = min(substitution, insertion, deletion)
    wer = dp[len(reference_words)][len(hypothesis_words)] / float(N)
    return wer


def recognize_speech_from_url(audio_url: str) -> str:
    recognizer = sr.Recognizer()
    audio_data = requests.get(audio_url).content
    audio_file = BytesIO(audio_data)
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        recognized_text = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        recognized_text = ""
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        recognized_text = ""
    return recognized_text


def evaluate_test_set(csv_file_path: str) -> float:
    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    total_wer = 0
    num_files = len(df)

    for index, row in df.iterrows():
        audio_url = row['Audio:FILE']
        reference_text = row['Text:LABEL']

        # Recognize the speech from the audio URL
        hypothesis_text = recognize_speech_from_url(audio_url)

        # Calculate the WER for this audio file
        wer = calculate_wer(reference_text, hypothesis_text)
        total_wer += wer

        print(f"Audio {index + 1}:")
        print(f"Reference: {reference_text}")
        print(f"Hypothesis: {hypothesis_text}")
        print(f"WER: {wer:.2%}\n")

        # Average WER over all files
    average_wer = total_wer / num_files
    return average_wer

if __name__ == '__main__':
    model = AutoModel(model="")
    # Example usage
    csv_file_path = 'mydata_2/test_all.csv'  # Update with your actual CSV file path
    average_wer = evaluate_test_set(csv_file_path, model)
    print(f"Average Word Error Rate (WER) for the test set: {average_wer:.2%}")
