// Video.h
#pragma once

#include "CoreMinimal.h"
#include "Video.generated.h"

UCLASS()
class YOURPROJECT_API UVideo : public UObject {
    GENERATED_BODY()

public:
    UVideo();

    UFUNCTION(BlueprintCallable, Category = "Video")
    void Play();

    UFUNCTION(BlueprintCallable, Category = "Video")
    void Stop();
}
