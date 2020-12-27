def test(landmark):
    recommended_landmarks = []
    for i in range(10):
        recommended_landmarks.append(landmark+'_test'+str(i+1))
    return recommended_landmarks


print(test('경복궁'))