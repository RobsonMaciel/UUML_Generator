// Map.h
#pragma once

#include "CoreMinimal.h"
#include "Map.generated.h"

UCLASS()
class YOURPROJECT_API AMap {
    GENERATED_BODY()

public:
    AMap();

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Map")
    FString Name;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Map")
    TArray<class ALevel*> Levels;

    UFUNCTION(BlueprintCallable, Category = "Map")
    void LoadMap();

    UFUNCTION(BlueprintCallable, Category = "Map")
    void UnloadMap();
}
