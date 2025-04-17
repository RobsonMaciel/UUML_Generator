// AudioManager.h
#pragma once

#include "CoreMinimal.h"
#include "AudioManager.generated.h"

UCLASS()
class YOURPROJECT_API AAudioManager {
    GENERATED_BODY()

public:
    AAudioManager();

    UFUNCTION(BlueprintCallable, Category = "Audio")
    void PlaySound(FString soundName);

    UFUNCTION(BlueprintCallable, Category = "Audio")
    void StopSound(FString soundName);

    UFUNCTION(BlueprintCallable, Category = "Audio")
    void SetVolume(float volume);

    UFUNCTION(BlueprintCallable, Category = "Audio")
    void PlayMusic(FString musicName);
}
