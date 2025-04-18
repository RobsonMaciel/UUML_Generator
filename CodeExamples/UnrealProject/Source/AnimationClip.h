// AnimationClip.h
#pragma once

#include "CoreMinimal.h"
#include "AnimationClip.generated.h"

UCLASS()
class YOURPROJECT_API UAnimationClip : public UObject {
    GENERATED_BODY()

public:
    UAnimationClip();

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Animation")
    FString Name;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Animation")
    float Duration;

    UFUNCTION(BlueprintCallable, Category = "Animation")
    void Play();
}
