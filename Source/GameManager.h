// GameManager.h
#pragma once

#include "CoreMinimal.h"
#include "GameManager.generated.h"

UCLASS()
class YOURPROJECT_API AGameManager {
    GENERATED_BODY()

public:
    AGameManager();

    UFUNCTION(BlueprintCallable, Category = "Game")
    void StartGame();

    UFUNCTION(BlueprintCallable, Category = "Game")
    void EndGame();

    UFUNCTION(BlueprintCallable, Category = "Game")
    void SaveProgress();

    UFUNCTION(BlueprintCallable, Category = "Game")
    void LoadProgress();

    UFUNCTION(BlueprintCallable, Category = "Game")
    void RestartLevel();

    UFUNCTION(BlueprintCallable, Category = "Game")
    void LoadLevel(class ALevel* level);
}
