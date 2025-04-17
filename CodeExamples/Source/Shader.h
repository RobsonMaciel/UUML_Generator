// Shader.h
#pragma once

#include "CoreMinimal.h"
#include "Shader.generated.h"

UCLASS()
class YOURPROJECT_API UShader : public UObject {
    GENERATED_BODY()

public:
    UShader();

    UFUNCTION(BlueprintCallable, Category = "Shader")
    void Compile();

    UFUNCTION(BlueprintCallable, Category = "Shader")
    void SetProperty(FString propertyName, float value);
}
