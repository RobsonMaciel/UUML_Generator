// GameSettings.h
#pragma once

#include "CoreMinimal.h"
#include "GameSettings.generated.h"

UCLASS()
class YOURPROJECT_API AGameSettings {
    GENERATED_BODY()

public:
    AGameSettings();

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Settings")
    float Volume;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Settings")
    bool Fullscreen;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Settings")
    int ResolutionWidth;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Settings")
    int ResolutionHeight;

    UFUNCTION(BlueprintCallable, Category = "Settings")
    void ApplySettings();
}
