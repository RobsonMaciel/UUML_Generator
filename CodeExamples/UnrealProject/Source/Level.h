// Level.h
#pragma once

#include "CoreMinimal.h"
#include "Level.generated.h"

UCLASS()
class YOURPROJECT_API ALevel {
    GENERATED_BODY()

public:
    ALevel();

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Level")
    FString Name;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Level")
    int Difficulty;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Level")
    TArray<class AEnemy*> Enemies;

    UFUNCTION(BlueprintCallable, Category = "Level")
    void LoadLevel();

    UFUNCTION(BlueprintCallable, Category = "Level")
    void UnloadLevel();

    UFUNCTION(BlueprintCallable, Category = "Level")
    void SetWeather(FString weatherType);
}
