// Light.h
#pragma once

#include "CoreMinimal.h"
#include "Light.generated.h"

UCLASS()
class YOURPROJECT_API ALight {
    GENERATED_BODY()

public:
    ALight();

    UFUNCTION(BlueprintCallable, Category = "Lighting")
    void TurnOn();

    UFUNCTION(BlueprintCallable, Category = "Lighting")
    void TurnOff();

    UFUNCTION(BlueprintCallable, Category = "Lighting")
    void SetIntensity(float intensity);
}
