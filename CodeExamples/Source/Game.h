// Game.h
#pragma once

#include "CoreMinimal.h"
#include "Game.generated.h"

UCLASS()
class YOURPROJECT_API AGame {
    GENERATED_BODY()

public:
    AGame();

    UFUNCTION(BlueprintCallable, Category = "Game")
    void Start();

    UFUNCTION(BlueprintCallable, Category = "Game")
    void Stop();

    UFUNCTION(BlueprintCallable, Category = "Game")
    void Pause();

    UFUNCTION(BlueprintCallable, Category = "Game")
    void Resume();
}
