// Tutorial.h
#pragma once

#include "CoreMinimal.h"
#include "Tutorial.generated.h"

UCLASS()
class YOURPROJECT_API ATutorial {
    GENERATED_BODY()

public:
    ATutorial();

    UFUNCTION(BlueprintCallable, Category = "Tutorial")
    void ShowTutorial();

    UFUNCTION(BlueprintCallable, Category = "Tutorial")
    void HideTutorial();

    UFUNCTION(BlueprintCallable, Category = "Tutorial")
    void CompleteTutorial();
}
