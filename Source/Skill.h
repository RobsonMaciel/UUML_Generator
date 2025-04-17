// Skill.h
#pragma once

#include "CoreMinimal.h"
#include "Skill.generated.h"

UCLASS()
class YOURPROJECT_API ASkill {
    GENERATED_BODY()

public:
    ASkill();

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Skill")
    FString Name;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Skill")
    int Power;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Skill")
    float Cooldown;

    UFUNCTION(BlueprintCallable, Category = "Skill")
    void Use();

    UFUNCTION(BlueprintCallable, Category = "Skill")
    void Upgrade();
}
