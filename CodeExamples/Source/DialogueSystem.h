// DialogueSystem.h
#pragma once

#include "CoreMinimal.h"
#include "DialogueSystem.generated.h"

UCLASS()
class YOURPROJECT_API ADialogueSystem {
    GENERATED_BODY()

public:
    ADialogueSystem();

    UFUNCTION(BlueprintCallable, Category = "Dialogue")
    void ShowDialogue(FString dialogue);

    UFUNCTION(BlueprintCallable, Category = "Dialogue")
    void HideDialogue();

    UFUNCTION(BlueprintCallable, Category = "Dialogue")
    void DisplayChoices(TArray<FString> choices);
}
