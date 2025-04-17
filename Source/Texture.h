// Texture.h
#pragma once

#include "CoreMinimal.h"
#include "Texture.generated.h"

UCLASS()
class YOURPROJECT_API UTexture : public UObject {
    GENERATED_BODY()

public:
    UTexture();

    UFUNCTION(BlueprintCallable, Category = "Texture")
    void Load();

    UFUNCTION(BlueprintCallable, Category = "Texture")
    void Apply();
}
