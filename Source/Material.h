// Material.h
#pragma once

#include "CoreMinimal.h"
#include "Material.generated.h"

UCLASS()
class YOURPROJECT_API UMaterial : public UObject {
    GENERATED_BODY()

public:
    UMaterial();

    UFUNCTION(BlueprintCallable, Category = "Material")
    void Apply();

    UFUNCTION(BlueprintCallable, Category = "Material")
    void SetColor(FColor color);
}
