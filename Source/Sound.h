// Sound.h
#pragma once

#include "CoreMinimal.h"
#include "Sound.generated.h"

UCLASS()
class YOURPROJECT_API USound : public UObject {
    GENERATED_BODY()

public:
    USound();

    UFUNCTION(BlueprintCallable, Category = "Sound")
    void Play();

    UFUNCTION(BlueprintCallable, Category = "Sound")
    void Stop();
}
