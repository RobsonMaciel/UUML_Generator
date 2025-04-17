// Music.h
#pragma once

#include "CoreMinimal.h"
#include "Music.generated.h"

UCLASS()
class YOURPROJECT_API UMusic : public UObject {
    GENERATED_BODY()

public:
    UMusic();

    UFUNCTION(BlueprintCallable, Category = "Music")
    void Play();

    UFUNCTION(BlueprintCallable, Category = "Music")
    void Stop();
}
