model_name = "resnet"
epochs = 5
best_loss = 1.0
history = []

for epoch in range(1, epochs + 1):
    loss = round(1.0 / epoch, 3)
    history.append(loss)
    if loss < best_loss:
        best_loss = loss
        status = "improved"
    else:
        status = "no change"
    print(f"{model_name} epoch {epoch}: loss={loss} ({status})")

if best_loss < 0.25:
    print("good enough")
else:
    print("keep training")
print(f"best={best_loss} after {len(history)} epochs")
