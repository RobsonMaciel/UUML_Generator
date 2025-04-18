// Renderer.h
#pragma once

#include "CoreMinimal.h"
#include "Renderer.generated.h"

UCLASS()
class YOURPROJECT_API ARenderer {
    GENERATED_BODY()

public:
    ARenderer();

    UFUNCTION(BlueprintCallable, Category = "Rendering")
    void Render();

    UFUNCTION(BlueprintCallable, Category = "Rendering")
    void SetMaterial(class UMaterial* material);
}
