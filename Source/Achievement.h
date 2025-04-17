// Achievement.h
#pragma once

#include "CoreMinimal.h"
#include "Achievement.generated.h"

UCLASS()
class YOURPROJECT_API AAchievement {
    GENERATED_BODY()

public:
    AAchievement();

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Achievement")
    FString Title;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Achievement")
    FString Description;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Achievement")
    bool IsUnlocked;

    UFUNCTION(BlueprintCallable, Category = "Achievement")
    void Unlock();

    UFUNCTION(BlueprintCallable, Category = "Achievement")
    void Reset();
}
