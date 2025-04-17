// Mesh.h
#pragma once

#include "CoreMinimal.h"
#include "Mesh.generated.h"

UCLASS()
class YOURPROJECT_API UMesh : public UObject {
    GENERATED_BODY()

public:
    UMesh();

    UFUNCTION(BlueprintCallable, Category = "Mesh")
    void Render();

    UFUNCTION(BlueprintCallable, Category = "Mesh")
    void SetVertices(TArray<FVector> vertices);
}
