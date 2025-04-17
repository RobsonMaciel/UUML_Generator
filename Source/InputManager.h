// InputManager.h
#pragma once

#include "CoreMinimal.h"
#include "InputManager.generated.h"

UCLASS()
class YOURPROJECT_API AInputManager {
    GENERATED_BODY()

public:
    AInputManager();

    UFUNCTION(BlueprintCallable, Category = "Input")
    void ProcessInput();

    UFUNCTION(BlueprintCallable, Category = "Input")
    void MapInput(FString action, FString key);
}
