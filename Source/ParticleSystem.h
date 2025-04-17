// ParticleSystem.h
#pragma once

#include "CoreMinimal.h"
#include "ParticleSystem.generated.h"

UCLASS()
class YOURPROJECT_API AParticleSystem {
    GENERATED_BODY()

public:
    AParticleSystem();

    UFUNCTION(BlueprintCallable, Category = "Effects")
    void PlayEffect(FString effectName);

    UFUNCTION(BlueprintCallable, Category = "Effects")
    void StopEffect(FString effectName);

    UFUNCTION(BlueprintCallable, Category = "Effects")
    void SetEffectDuration(float duration);
}
