from specialists.vqa import answer_question

image = "data/Before/kochi_before.tif"

question = "What is in this image?"

answer = answer_question(image, question)

print("Question:", question)
print("Answer:", answer)