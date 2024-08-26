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
define void @_Z10int_othersv() #0 {
  %1 = alloca i32, align 4
  %2 = alloca i16, align 2
  %3 = alloca float, align 4
  %4 = load i32, ptr %1, align 4
  %5 = load i16, ptr %2, align 2
  %6 = sext i16 %5 to i32
  %7 = add nsw i32 %4, %6
  %8 = load i16, ptr %2, align 2
  %9 = sext i16 %8 to i32
  %10 = load i32, ptr %1, align 4
  %11 = add nsw i32 %9, %10
  %12 = load i32, ptr %1, align 4
  %13 = sitofp i32 %12 to float
  %14 = load float, ptr %3, align 4
  %15 = fadd float %13, %14
  %16 = load float, ptr %3, align 4
  %17 = load i32, ptr %1, align 4
  %18 = sitofp i32 %17 to float
  %19 = fadd float %16, %18
  ret void
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
define void @_Z12float_othersv() #0 {
  %1 = alloca i32, align 4
  %2 = alloca i16, align 2
  %3 = alloca float, align 4
  %4 = load float, ptr %3, align 4
  %5 = load i16, ptr %2, align 2
  %6 = sext i16 %5 to i32
  %7 = sitofp i32 %6 to float
  %8 = fadd float %4, %7
  %9 = load i16, ptr %2, align 2
  %10 = sext i16 %9 to i32
  %11 = sitofp i32 %10 to float
  %12 = load float, ptr %3, align 4
  %13 = fadd float %11, %12
  %14 = load float, ptr %3, align 4
  %15 = load i32, ptr %1, align 4
  %16 = sitofp i32 %15 to float
  %17 = fadd float %14, %16
  %18 = load i32, ptr %1, align 4
  %19 = sitofp i32 %18 to float
  %20 = load float, ptr %3, align 4
  %21 = fadd float %19, %20
  ret void
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

; Function Attrs: mustprogress noinline nounwind optnone ssp uwtable(sync)
define void @_Z12short_othersv() #0 {
  %1 = alloca i32, align 4
  %2 = alloca i16, align 2
  %3 = alloca float, align 4
  %4 = load i16, ptr %2, align 2
  %5 = sext i16 %4 to i32
  %6 = sitofp i32 %5 to float
  %7 = load float, ptr %3, align 4
  %8 = fadd float %6, %7
  %9 = load float, ptr %3, align 4
  %10 = load i16, ptr %2, align 2
  %11 = sext i16 %10 to i32
  %12 = sitofp i32 %11 to float
  %13 = fadd float %9, %12
  %14 = load i16, ptr %2, align 2
  %15 = sext i16 %14 to i32
  %16 = load i32, ptr %1, align 4
  %17 = add nsw i32 %15, %16
  %18 = load i32, ptr %1, align 4
  %19 = load i16, ptr %2, align 2
  %20 = sext i16 %19 to i32
  %21 = add nsw i32 %18, %20
  ret void
}

; Function Attrs: mustprogress noinline norecurse optnone ssp uwtable(sync)
define noundef i32 @main() #1 {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  %3 = alloca float, align 4
  %4 = alloca i16, align 2
  store i32 0, ptr %1, align 4
  %5 = call noundef i32 @_Z7int_sumii(i32 noundef 23, i32 noundef 13)
  store i32 %5, ptr %2, align 4
  %6 = call noundef float @_Z9float_sumff(float noundef 0x40091EB860000000, float noundef 0x4005AE1480000000)
  store float %6, ptr %3, align 4
  %7 = call noundef signext i16 @_Z9short_sumss(i16 noundef signext 1, i16 noundef signext 2)
  store i16 %7, ptr %4, align 2
  %8 = load i32, ptr %2, align 4
  %9 = sitofp i32 %8 to float
  %10 = load float, ptr %3, align 4
  %11 = fadd float %9, %10
  %12 = load i16, ptr %4, align 2
  %13 = sext i16 %12 to i32
  %14 = sitofp i32 %13 to float
  %15 = fadd float %11, %14
  %16 = fptosi float %15 to i32
  %17 = call i32 (ptr, ...) @printf(ptr noundef @.str, i32 noundef %16)
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
