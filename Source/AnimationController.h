// AnimationController.h
#pragma once

#include "CoreMinimal.h"
#include "AnimationController.generated.h"

UCLASS()
class YOURPROJECT_API AAnimationController {
    GENERATED_BODY()

public:
    AAnimationController();

    UFUNCTION(BlueprintCallable, Category = "Animation")
    void PlayAnimation(FString animationName);

    UFUNCTION(BlueprintCallable, Category = "Animation")
    void StopAnimation();

    UFUNCTION(BlueprintCallable, Category = "Animation")
    void SetAnimationSpeed(float speed);

    UFUNCTION(BlueprintCallable, Category = "Animation")
    void ResetAnimation();
}
