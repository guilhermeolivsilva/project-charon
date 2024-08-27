; ModuleID = 'llvm_type_cast.cpp'
source_filename = "llvm_type_cast.cpp"
target datalayout = "e-m:o-i64:64-i128:128-n32:64-S128"
target triple = "arm64-apple-macosx14.0.0"

@.str = private unnamed_addr constant [3 x i8] c"%d\00", align 1

; Function Attrs: mustprogress noinline nounwind optnone ssp uwtable(sync)
define noundef i32 @_Z7int_sumii(i32 noundef %0, i32 noundef %1) #0 {
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  store i32 %0, ptr %3, align 4
  store i32 %1, ptr %4, align 4
  %5 = load i32, ptr %3, align 4
  %6 = load i32, ptr %4, align 4
  %7 = add nsw i32 %5, %6
  ret i32 %7
}

; Function Attrs: mustprogress noinline nounwind optnone ssp uwtable(sync)
define noundef float @_Z9float_sumff(float noundef %0, float noundef %1) #0 {
  %3 = alloca float, align 4
  %4 = alloca float, align 4
  store float %0, ptr %3, align 4
  store float %1, ptr %4, align 4
  %5 = load float, ptr %3, align 4
  %6 = load float, ptr %4, align 4
  %7 = fadd float %5, %6
  ret float %7
}

; Function Attrs: mustprogress noinline nounwind optnone ssp uwtable(sync)
define noundef signext i16 @_Z9short_sumss(i16 noundef signext %0, i16 noundef signext %1) #0 {
  %3 = alloca i16, align 2
  %4 = alloca i16, align 2
  store i16 %0, ptr %3, align 2
  store i16 %1, ptr %4, align 2
  %5 = load i16, ptr %3, align 2
  %6 = sext i16 %5 to i32
  %7 = load i16, ptr %4, align 2
  %8 = sext i16 %7 to i32
  %9 = add nsw i32 %6, %8
  %10 = trunc i32 %9 to i16
  ret i16 %10
}

; Function Attrs: mustprogress noinline norecurse optnone ssp uwtable(sync)
define noundef i32 @main() #1 {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  %3 = alloca float, align 4
  %4 = alloca i16, align 2
  %5 = alloca i16, align 2
  %6 = alloca i16, align 2
  %7 = alloca i32, align 4
  %8 = alloca i32, align 4
  %9 = alloca float, align 4
  %10 = alloca float, align 4
  store i32 0, ptr %1, align 4
  %11 = call noundef i32 @_Z7int_sumii(i32 noundef 23, i32 noundef 13)
  store i32 %11, ptr %2, align 4
  %12 = call noundef float @_Z9float_sumff(float noundef 0x40091EB860000000, float noundef 0x4005AE1480000000)
  store float %12, ptr %3, align 4
  %13 = call noundef signext i16 @_Z9short_sumss(i16 noundef signext 1, i16 noundef signext 2)
  store i16 %13, ptr %4, align 2
  %14 = load i32, ptr %2, align 4
  %15 = sitofp i32 %14 to float
  %16 = load float, ptr %3, align 4
  %17 = fadd float %15, %16
  %18 = load i16, ptr %4, align 2
  %19 = sext i16 %18 to i32
  %20 = sitofp i32 %19 to float
  %21 = fadd float %17, %20
  %22 = fptosi float %21 to i32
  %23 = call i32 (ptr, ...) @printf(ptr noundef @.str, i32 noundef %22)
  %24 = load i32, ptr %2, align 4
  %25 = sitofp i32 %24 to float
  %26 = load float, ptr %3, align 4
  %27 = load i16, ptr %4, align 2
  %28 = sext i16 %27 to i32
  %29 = sitofp i32 %28 to float
  %30 = fadd float %26, %29
  %31 = fadd float %25, %30
  %32 = fptosi float %31 to i16
  store i16 %32, ptr %5, align 2
  %33 = load i32, ptr %2, align 4
  %34 = mul nsw i32 2, %33
  %35 = load i16, ptr %4, align 2
  %36 = sext i16 %35 to i32
  %37 = mul nsw i32 %34, %36
  %38 = sitofp i32 %37 to float
  %39 = load float, ptr %3, align 4
  %40 = fmul float %38, %39
  %41 = fptosi float %40 to i16
  store i16 %41, ptr %6, align 2
  %42 = load i32, ptr %2, align 4
  %43 = sitofp i32 %42 to float
  %44 = load float, ptr %3, align 4
  %45 = load i16, ptr %4, align 2
  %46 = sext i16 %45 to i32
  %47 = sitofp i32 %46 to float
  %48 = fadd float %44, %47
  %49 = fadd float %43, %48
  %50 = fptosi float %49 to i32
  store i32 %50, ptr %7, align 4
  %51 = load i32, ptr %2, align 4
  %52 = mul nsw i32 2, %51
  %53 = load i16, ptr %4, align 2
  %54 = sext i16 %53 to i32
  %55 = mul nsw i32 %52, %54
  %56 = sitofp i32 %55 to float
  %57 = load float, ptr %3, align 4
  %58 = fmul float %56, %57
  %59 = fptosi float %58 to i32
  store i32 %59, ptr %8, align 4
  %60 = load i32, ptr %2, align 4
  %61 = load i16, ptr %4, align 2
  %62 = sext i16 %61 to i32
  %63 = add nsw i32 %60, %62
  %64 = sitofp i32 %63 to float
  store float %64, ptr %9, align 4
  %65 = load i32, ptr %2, align 4
  %66 = mul nsw i32 2, %65
  %67 = load i16, ptr %4, align 2
  %68 = sext i16 %67 to i32
  %69 = mul nsw i32 %66, %68
  %70 = sitofp i32 %69 to float
  store float %70, ptr %10, align 4
  ret i32 0
}

declare i32 @printf(ptr noundef, ...) #2

attributes #0 = { mustprogress noinline nounwind optnone ssp uwtable(sync) "frame-pointer"="non-leaf" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="apple-m1" "target-features"="+aes,+crc,+dotprod,+fp-armv8,+fp16fml,+fullfp16,+lse,+neon,+ras,+rcpc,+rdm,+sha2,+sha3,+v8.1a,+v8.2a,+v8.3a,+v8.4a,+v8.5a,+v8a,+zcm,+zcz" }
attributes #1 = { mustprogress noinline norecurse optnone ssp uwtable(sync) "frame-pointer"="non-leaf" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="apple-m1" "target-features"="+aes,+crc,+dotprod,+fp-armv8,+fp16fml,+fullfp16,+lse,+neon,+ras,+rcpc,+rdm,+sha2,+sha3,+v8.1a,+v8.2a,+v8.3a,+v8.4a,+v8.5a,+v8a,+zcm,+zcz" }
attributes #2 = { "frame-pointer"="non-leaf" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="apple-m1" "target-features"="+aes,+crc,+dotprod,+fp-armv8,+fp16fml,+fullfp16,+lse,+neon,+ras,+rcpc,+rdm,+sha2,+sha3,+v8.1a,+v8.2a,+v8.3a,+v8.4a,+v8.5a,+v8a,+zcm,+zcz" }

!llvm.module.flags = !{!0, !1, !2, !3}
!llvm.ident = !{!4}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{i32 8, !"PIC Level", i32 2}
!2 = !{i32 7, !"uwtable", i32 1}
!3 = !{i32 7, !"frame-pointer", i32 1}
!4 = !{!"Homebrew clang version 17.0.3"}
