// Spell.h
#pragma once

#include "CoreMinimal.h"
#include "Spell.generated.h"

UCLASS()
class YOURPROJECT_API ASpell {
    GENERATED_BODY()

public:
    ASpell();

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Spell")
    FString Name;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Spell")
    int ManaCost;

    UFUNCTION(BlueprintCallable, Category = "Spell")
    void Cast();

    UFUNCTION(BlueprintCallable, Category = "Spell")
    void Cancel();
}
